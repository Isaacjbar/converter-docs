# Plan de Pruebas de Seguridad — Java-to-UML Converter

**Versión:** 1.0  
**Fecha:** 2026-04-08  
**Clasificación:** Interno  
**Proyecto:** Converter (service-converter + converter-web-app)

---

## 1. Objetivo

Verificar que el sistema es resistente a ataques comunes de seguridad web en sus tres módulos principales: **Accounts**, **Converter** e **History**, garantizando confidencialidad, integridad y control de acceso adecuado.

---

## 2. Alcance

| Módulo | Componente | Endpoints cubiertos |
|--------|-----------|---------------------|
| Accounts | Autenticación y gestión de usuarios | `POST /auth/register/`, `POST /auth/login/`, `POST /auth/refresh/`, `GET /auth/me/`, `GET /auth/users/`, `PATCH /auth/users/{id}/`, `DELETE /auth/users/{id}/` |
| Converter | Conversión Java → UML | `POST /convert/`, `GET /examples/` |
| History | Historial de conversiones | `GET /history/`, `GET /history/{id}/`, `DELETE /history/{id}/` |

---

## 3. Entorno de Pruebas

| Elemento | Valor |
|----------|-------|
| Backend URL | `http://localhost:8000/api` |
| Frontend URL | `http://localhost:5173` |
| Herramienta principal | Postman / cURL / OWASP ZAP |
| Base de datos | SQLite3 (`db.sqlite3`) |
| Autenticación | JWT (SimpleJWT — access: 12h, refresh: 7d) |

---

## 4. Tipos de Prueba

- **Seguridad** — control de acceso, inyección, escalación de privilegios
- **Funcional** — comportamiento esperado ante entradas válidas/inválidas
- **Borde** — valores límite, payloads vacíos o malformados

---

## 5. Pruebas por Módulo

---

### 5.1 Módulo Accounts

#### PT-ACC-01 — Acceso a endpoint protegido sin token ✅

| Campo | Detalle |
|-------|---------|
| **ID** | PT-ACC-01 |
| **Tipo** | Seguridad |
| **Prioridad** | Alta |
| **Precondición** | Sin token en los headers |
| **Endpoint** | `GET /auth/me/` |
| **Método** | GET |
| **Headers** | *(ninguno)* |
| **Resultado esperado** | `401 Unauthorized` con mensaje de autenticación requerida |
| **Resultado obtenido** | `401 Unauthorized` |
| **Estado** | PASS |

---

#### PT-ACC-02 — Login con credenciales inválidas ✅

| Campo | Detalle |
|-------|---------|
| **ID** | PT-ACC-02 |
| **Tipo** | Seguridad / Funcional |
| **Prioridad** | Alta |
| **Precondición** | Usuario existente en la base de datos |
| **Endpoint** | `POST /auth/login/` |
| **Método** | POST |
| **Body** | `{ "email": "user@test.com", "password": "wrong_password" }` |
| **Resultado esperado** | `401 Unauthorized`, sin tokens en la respuesta |
| **Resultado obtenido** | `401 Unauthorized` |
| **Estado** | PASS |

---

#### PT-ACC-03 — Registro con datos duplicados (email existente)

| Campo | Detalle |
|-------|---------|
| **ID** | PT-ACC-03 |
| **Tipo** | Funcional / Seguridad |
| **Prioridad** | Media |
| **Precondición** | Usuario con email `duplicate@test.com` ya registrado |
| **Endpoint** | `POST /auth/register/` |
| **Método** | POST |
| **Body** | `{ "email": "duplicate@test.com", "username": "otro", "password": "123456" }` |
| **Resultado esperado** | `400 Bad Request` indicando email duplicado; no se crea segundo usuario |
| **Resultado obtenido** | — |
| **Estado** | PENDIENTE |

---

#### PT-ACC-04 — Acceso a endpoint de administración con rol analista

| Campo | Detalle |
|-------|---------|
| **ID** | PT-ACC-04 |
| **Tipo** | Seguridad (escalación de privilegios) |
| **Prioridad** | Crítica |
| **Precondición** | Token JWT válido de usuario con `role=analyst` |
| **Endpoint** | `GET /auth/users/` |
| **Método** | GET |
| **Headers** | `Authorization: Bearer <analyst_token>` |
| **Resultado esperado** | `403 Forbidden` — sólo admins pueden listar usuarios |
| **Resultado obtenido** | — |
| **Estado** | PENDIENTE |

---

#### PT-ACC-05 — Modificación de otro usuario con rol analista

| Campo | Detalle |
|-------|---------|
| **ID** | PT-ACC-05 |
| **Tipo** | Seguridad (IDOR / escalación de privilegios) |
| **Prioridad** | Crítica |
| **Precondición** | Token JWT válido de `analyst`, conociendo el `id` de otro usuario |
| **Endpoint** | `PATCH /auth/users/{otro_id}/` |
| **Método** | PATCH |
| **Headers** | `Authorization: Bearer <analyst_token>` |
| **Body** | `{ "role": "admin" }` |
| **Resultado esperado** | `403 Forbidden` — analistas no pueden modificar usuarios |
| **Resultado obtenido** | — |
| **Estado** | PENDIENTE |

---

#### PT-ACC-06 — Uso de token expirado

| Campo | Detalle |
|-------|---------|
| **ID** | PT-ACC-06 |
| **Tipo** | Seguridad |
| **Prioridad** | Alta |
| **Precondición** | Access token expirado (>12h), refresh token válido |
| **Endpoint** | `GET /auth/me/` |
| **Método** | GET |
| **Headers** | `Authorization: Bearer <expired_access_token>` |
| **Resultado esperado** | `401 Unauthorized`; el frontend debe renovar automáticamente con el refresh token |
| **Resultado obtenido** | — |
| **Estado** | PENDIENTE |

---

#### PT-ACC-07 — Inyección SQL en login

| Campo | Detalle |
|-------|---------|
| **ID** | PT-ACC-07 |
| **Tipo** | Seguridad (SQL Injection) |
| **Prioridad** | Crítica |
| **Precondición** | Ninguna |
| **Endpoint** | `POST /auth/login/` |
| **Método** | POST |
| **Body** | `{ "email": "' OR '1'='1", "password": "' OR '1'='1" }` |
| **Resultado esperado** | `401 Unauthorized`; sin acceso al sistema |
| **Resultado obtenido** | — |
| **Estado** | PENDIENTE |

---

### 5.2 Módulo Converter

#### PT-CNV-01 — Envío de código malformado / vacío ✅

| Campo | Detalle |
|-------|---------|
| **ID** | PT-CNV-01 |
| **Tipo** | Funcional / Borde |
| **Prioridad** | Media |
| **Precondición** | Token JWT válido |
| **Endpoint** | `POST /convert/` |
| **Método** | POST |
| **Headers** | `Authorization: Bearer <token>` |
| **Body** | FormData con campo `code` = `""` (vacío) |
| **Resultado esperado** | `400 Bad Request` con mensaje de error descriptivo |
| **Resultado obtenido** | `400 Bad Request` |
| **Estado** | PASS |

---

#### PT-CNV-02 — Conversión sin autenticación (verificar guardado en historial)

| Campo | Detalle |
|-------|---------|
| **ID** | PT-CNV-02 |
| **Tipo** | Seguridad / Funcional |
| **Prioridad** | Media |
| **Precondición** | Sin token JWT |
| **Endpoint** | `POST /convert/` |
| **Método** | POST |
| **Body** | FormData con código Java válido |
| **Resultado esperado** | `401 Unauthorized` — el endpoint requiere autenticación |
| **Resultado obtenido** | — |
| **Estado** | PENDIENTE |

---

#### PT-CNV-03 — Subida de archivo con extensión incorrecta

| Campo | Detalle |
|-------|---------|
| **ID** | PT-CNV-03 |
| **Tipo** | Seguridad / Borde |
| **Prioridad** | Alta |
| **Precondición** | Token JWT válido |
| **Endpoint** | `POST /convert/` |
| **Método** | POST |
| **Headers** | `Authorization: Bearer <token>` |
| **Body** | FormData con archivo `malicious.php` o `script.exe` |
| **Resultado esperado** | `400 Bad Request` rechazando extensiones no permitidas |
| **Resultado obtenido** | — |
| **Estado** | PENDIENTE |

---

#### PT-CNV-04 — Subida de ZIP con path traversal

| Campo | Detalle |
|-------|---------|
| **ID** | PT-CNV-04 |
| **Tipo** | Seguridad (Path Traversal) |
| **Prioridad** | Crítica |
| **Precondición** | Token JWT válido |
| **Endpoint** | `POST /convert/` |
| **Método** | POST |
| **Headers** | `Authorization: Bearer <token>` |
| **Body** | FormData con archivo ZIP que contiene entradas como `../../etc/passwd` |
| **Resultado esperado** | `400 Bad Request` o extracción segura ignorando rutas fuera del directorio temporal |
| **Resultado obtenido** | — |
| **Estado** | PENDIENTE |

---

#### PT-CNV-05 — Inyección de código en payload de conversión (SSTI)

| Campo | Detalle |
|-------|---------|
| **ID** | PT-CNV-05 |
| **Tipo** | Seguridad (Server-Side Template Injection) |
| **Prioridad** | Alta |
| **Precondición** | Token JWT válido |
| **Endpoint** | `POST /convert/` |
| **Método** | POST |
| **Headers** | `Authorization: Bearer <token>` |
| **Body** | FormData con `code` = `{{ 7*7 }}` o `${7*7}` |
| **Resultado esperado** | Respuesta normal de parsing; sin ejecución de expresión |
| **Resultado obtenido** | — |
| **Estado** | PENDIENTE |

---

#### PT-CNV-06 — Cuerpo cifrado con clave AES incorrecta

| Campo | Detalle |
|-------|---------|
| **ID** | PT-CNV-06 |
| **Tipo** | Seguridad (integridad del canal) |
| **Prioridad** | Alta |
| **Precondición** | Token JWT válido |
| **Endpoint** | `POST /convert/` (o cualquier JSON endpoint) |
| **Método** | POST |
| **Headers** | `Authorization: Bearer <token>`, `X-Encrypted: true` |
| **Body** | Payload cifrado con clave AES diferente a la del servidor |
| **Resultado esperado** | `400 Bad Request` — fallo de descifrado por clave o tag inválidos |
| **Resultado obtenido** | — |
| **Estado** | PENDIENTE |

---

### 5.3 Módulo History

#### PT-HIS-01 — Acceso al historial de otro usuario ✅

| Campo | Detalle |
|-------|---------|
| **ID** | PT-HIS-01 |
| **Tipo** | Seguridad (IDOR) |
| **Prioridad** | Crítica |
| **Precondición** | Dos usuarios distintos con historial propio; se conoce el `id` de entrada del otro |
| **Endpoint** | `GET /history/{id_de_otro_usuario}/` |
| **Método** | GET |
| **Headers** | `Authorization: Bearer <token_usuario_A>` |
| **Resultado esperado** | `404 Not Found` — el sistema no devuelve registros de otro usuario |
| **Resultado obtenido** | `404 Not Found` |
| **Estado** | PASS |

---

#### PT-HIS-02 — Eliminar historial de otro usuario ✅

| Campo | Detalle |
|-------|---------|
| **ID** | PT-HIS-02 |
| **Tipo** | Seguridad (IDOR) |
| **Prioridad** | Crítica |
| **Precondición** | Dos usuarios distintos; se conoce el `id` de entrada del otro |
| **Endpoint** | `DELETE /history/{id_de_otro_usuario}/` |
| **Método** | DELETE |
| **Headers** | `Authorization: Bearer <token_usuario_A>` |
| **Resultado esperado** | `404 Not Found` — el sistema no permite eliminar registros ajenos |
| **Resultado obtenido** | `404 Not Found` |
| **Estado** | PASS |

---

#### PT-HIS-03 — Listado de historial sin autenticación

| Campo | Detalle |
|-------|---------|
| **ID** | PT-HIS-03 |
| **Tipo** | Seguridad |
| **Prioridad** | Alta |
| **Precondición** | Sin token JWT |
| **Endpoint** | `GET /history/` |
| **Método** | GET |
| **Headers** | *(ninguno)* |
| **Resultado esperado** | `401 Unauthorized` |
| **Resultado obtenido** | — |
| **Estado** | PENDIENTE |

---

#### PT-HIS-04 — Acceso a historial con token de otro módulo / token manipulado

| Campo | Detalle |
|-------|---------|
| **ID** | PT-HIS-04 |
| **Tipo** | Seguridad (JWT forgery) |
| **Prioridad** | Crítica |
| **Precondición** | Token JWT válido modificado manualmente (cambio de `user_id` en payload) |
| **Endpoint** | `GET /history/` |
| **Método** | GET |
| **Headers** | `Authorization: Bearer <tampered_token>` |
| **Resultado esperado** | `401 Unauthorized` — la firma JWT no es válida |
| **Resultado obtenido** | — |
| **Estado** | PENDIENTE |

---

#### PT-HIS-05 — Enumeración de IDs en historial

| Campo | Detalle |
|-------|---------|
| **ID** | PT-HIS-05 |
| **Tipo** | Seguridad (IDOR / enumeración) |
| **Prioridad** | Alta |
| **Precondición** | Token JWT válido de usuario analista |
| **Endpoint** | `GET /history/{id}/` iterando IDs 1..100 |
| **Método** | GET |
| **Headers** | `Authorization: Bearer <token>` |
| **Resultado esperado** | Sólo devuelve `200 OK` para IDs pertenecientes al usuario autenticado; `404` para el resto |
| **Resultado obtenido** | — |
| **Estado** | PENDIENTE |

---

#### PT-HIS-06 — Intento de inyección en parámetros de historial

| Campo | Detalle |
|-------|---------|
| **ID** | PT-HIS-06 |
| **Tipo** | Seguridad (SQL Injection / Query Injection) |
| **Prioridad** | Alta |
| **Precondición** | Token JWT válido |
| **Endpoint** | `GET /history/1 OR 1=1/` |
| **Método** | GET |
| **Headers** | `Authorization: Bearer <token>` |
| **Resultado esperado** | `404 Not Found` o `400 Bad Request` — sin datos inesperados expuestos |
| **Resultado obtenido** | — |
| **Estado** | PENDIENTE |

---

## 6. Resumen de Pruebas

| ID | Módulo | Descripción | Estado |
|----|--------|-------------|--------|
| PT-ACC-01 | Accounts | Acceso sin token | PASS ✅ |
| PT-ACC-02 | Accounts | Login con credenciales inválidas | PASS ✅ |
| PT-ACC-03 | Accounts | Registro con email duplicado | PENDIENTE |
| PT-ACC-04 | Accounts | Endpoint admin con rol analista | PENDIENTE |
| PT-ACC-05 | Accounts | Modificar otro usuario siendo analista | PENDIENTE |
| PT-ACC-06 | Accounts | Uso de token expirado | PENDIENTE |
| PT-ACC-07 | Accounts | SQL Injection en login | PENDIENTE |
| PT-CNV-01 | Converter | Código vacío / malformado | PASS ✅ |
| PT-CNV-02 | Converter | Conversión sin autenticación | PENDIENTE |
| PT-CNV-03 | Converter | Archivo con extensión incorrecta | PENDIENTE |
| PT-CNV-04 | Converter | ZIP con path traversal | PENDIENTE |
| PT-CNV-05 | Converter | Inyección SSTI en código fuente | PENDIENTE |
| PT-CNV-06 | Converter | Cuerpo cifrado con clave AES incorrecta | PENDIENTE |
| PT-HIS-01 | History | Acceso al historial de otro usuario | PASS ✅ |
| PT-HIS-02 | History | Eliminar historial de otro usuario | PASS ✅ |
| PT-HIS-03 | History | Listado sin autenticación | PENDIENTE |
| PT-HIS-04 | History | JWT manipulado / forjado | PENDIENTE |
| PT-HIS-05 | History | Enumeración de IDs | PENDIENTE |
| PT-HIS-06 | History | Inyección en parámetros de URL | PENDIENTE |

**Total:** 19 pruebas | **PASS:** 5 | **PENDIENTE:** 14

---

## 7. Criterios de Aceptación

| Criterio | Descripción |
|----------|-------------|
| Control de acceso | Todos los endpoints protegidos devuelven `401`/`403` sin credenciales válidas |
| Aislamiento de datos | Ningún usuario puede leer o modificar recursos de otro usuario |
| Validación de entrada | Entradas malformadas, vacías o con payloads de inyección son rechazadas con `400` |
| Integridad JWT | Tokens manipulados o expirados son rechazados correctamente |
| Seguridad de archivos | Archivos con extensión incorrecta o ZIPs con path traversal son bloqueados |
| Cifrado AES | Payloads con clave incorrecta son rechazados sin exponer información sensible |

---

## 8. Referencias

- [Documentación de Seguridad](./security.md)
- [Reporte DAST (OWASP ZAP)](./zap-dast.md)
- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
