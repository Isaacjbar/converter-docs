# Seguridad y Observabilidad

## Resumen

El sistema implementa tres capas de seguridad/observabilidad:

1. **AuditLog** — bitácora de base de datos
2. **Django Logger** — logs de requests y errores a archivo
3. **SHA-256 + AES-256-GCM** — integridad de datos y cifrado de payload entre back y front

---

## 1. Bitácora de BD — `AuditLog`

**App:** `apps/audit/`  
**Tabla:** `audit_auditlog`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `user` | FK → User, null | Quién realizó la acción |
| `action` | CharField | CREATE, UPDATE, DELETE, LOGIN, ACCESS, ERROR |
| `resource` | CharField | Modelo afectado: "DiagramHistory", "User" |
| `resource_id` | CharField, null | ID del objeto |
| `description` | TextField | Detalle legible |
| `ip_address` | GenericIPAddressField, null | IP del cliente |
| `checksum` | CharField(64) | SHA-256 de los campos de contenido |
| `created_at` | DateTimeField | Inmutable, auto |

**Checksum:** `sha256(user_id + action + resource + resource_id + description)` — permite detectar tampering offline.

**Cuándo se genera:**
- `post_save` / `post_delete` en `DiagramHistory` → CREATE, UPDATE, DELETE
- `post_save` / `post_delete` en `User` → CREATE, UPDATE, DELETE
- Login exitoso (`AuditedTokenObtainPairView`) → LOGIN

**Admin:** visible en `/admin/audit/auditlog/` como read-only.

---

## 2. Django Logger

**Archivos de log:** `logs/requests.log` y `logs/errors.log` (rotating, 10 MB, 5 backups).

| Logger | Nivel | Contenido |
|--------|-------|-----------|
| `converter.requests` | INFO | Cada request: método, path, user ID, IP, status code |
| `converter.errors` | ERROR | Excepciones con traceback completo |

**Middleware:** `RequestLoggingMiddleware` en `config/middleware.py` — corre antes de cada view, extrae IP y loguea entrada/salida.

**Views con error logging:**
- `apps/converter/views.py` — ZIP extraction y conversión
- `apps/accounts/views.py` — login fallido (implícito vía DRF)

**Formato de log:**
```
[2026-04-02 14:32:01] INFO converter.requests POST /convert/ user=3 ip=192.168.1.1
[2026-04-02 14:32:01] INFO converter.requests POST /convert/ → 200
[2026-04-02 14:32:05] ERROR converter.errors ConvertView.convert failed: ...traceback...
```

---

## 3. SHA-256

**Dos usos:**

### Checksum de AuditLog
Calculado en `AuditLog.save()` antes de insertar. Cubre los campos de contenido (no `created_at`).

### Hash de source_code en DiagramHistory
Campo `source_hash` (CharField 64) en `DiagramHistory` — SHA-256 del código Java fuente.  
Calculado automáticamente en `DiagramHistory.save()`.  
Útil para deduplicación y verificar integridad del código almacenado.

**Helper:** `utils/crypto.py → sha256(data: str) -> str`

---

## 4. AES-256-GCM — Cifrado de Payload

Cifra los cuerpos JSON entre el frontend React y el backend Django.

### Algoritmo
- **AES-256-GCM** (cifrado autenticado — confidencialidad + integridad)
- **IV/Nonce:** 12 bytes aleatorios por request
- **Formato wire:** `base64(nonce[12] + ciphertext + tag[16])`

### Configuración de llave

La llave es **compartida** entre backend y frontend. Se configura via variables de entorno:

| Proyecto | Variable | Archivo |
|----------|----------|---------|
| `service-converter` | `AES_SECRET_KEY` | `.env` |
| `converter-web-app` | `VITE_AES_KEY` | `.env` |

> **Importante:** ambas variables deben tener el mismo valor — 64 caracteres hex (= 32 bytes).

### Alcance del cifrado

| Tipo de request | ¿Cifrado? |
|-----------------|-----------|
| JSON body (POST/PATCH/PUT) | ✅ Sí |
| FormData / file uploads | ❌ No (binario multipart) |
| GET requests | ❌ No (sin body) |

### Flujo backend (`config/middleware.py → AESEncryptionMiddleware`)

```
Request con header X-Encrypted: true
  → Middleware descifra body → reemplaza request._body como JSON plano
  → View procesa normalmente
Response
  → Middleware cifra response.content
  → Retorna { "data": "<base64-ciphertext>" } con header X-Encrypted: true
```

### Flujo frontend (`src/api.js` + `src/utils/crypto.js`)

```
Request interceptor:
  Si config.data y no es FormData y no es GET
    → encryptPayload(data) → body cifrado
    → headers: X-Encrypted: true, Content-Type: text/plain

Response interceptor:
  Si header x-encrypted === 'true' y response.data.data existe
    → decryptPayload(response.data.data) → objeto JSON original
```

**Implementación frontend:** usa `crypto.subtle` (Web Crypto API nativa del browser, sin dependencias extra).

---

## Variables de entorno

### `service-converter/.env`
```env
AES_SECRET_KEY=<64 hex chars>
```

### `converter-web-app/.env`
```env
VITE_API_URL=http://localhost:8000/api
VITE_AES_KEY=<misma llave, 64 hex chars>
```

> Los archivos `.env` están en `.gitignore`. Para obtener una nueva llave: `python -c "import os; print(os.urandom(32).hex())"`

---

## Archivos relevantes

| Archivo | Responsabilidad |
|---------|----------------|
| `utils/crypto.py` | sha256(), encrypt_aes256(), decrypt_aes256() |
| `utils/request_context.py` | Thread-local para propagar IP del request a signals |
| `apps/audit/models.py` | Modelo AuditLog |
| `apps/audit/signals.py` | Handlers de signals para DiagramHistory y User |
| `apps/audit/admin.py` | Vista admin read-only |
| `config/middleware.py` | RequestLoggingMiddleware + AESEncryptionMiddleware |
| `src/utils/crypto.js` | encryptPayload(), decryptPayload() (Web Crypto API) |
| `src/api.js` | Interceptores de axios para cifrado/descifrado |
