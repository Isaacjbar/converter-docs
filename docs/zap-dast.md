# DAST — Pruebas de Seguridad Dinámicas con OWASP ZAP

Pruebas dinámicas ejecutadas contra los ambientes productivos usando OWASP ZAP en Docker.

---

## Resultados finales

### Backend — `api.converter.levsek.com.mx`

| Resultado | Cantidad |
|-----------|----------|
| PASS      | 118      |
| WARN      | 1        |
| FAIL      | 0        |

**Única advertencia (no explotable):**
Redirects 301 de Django en URLs sin trailing slash — comportamiento esperado del framework.

**Ataques que PASARON:**
SQL Injection, XSS Reflected/Persistent/DOM, Path Traversal, Remote Code Execution,
Command Injection, Buffer Overflow, CSRF, XXE, SSTI, Log4Shell, Spring4Shell,
LDAP Injection, Remote File Inclusion, CRLF Injection, Parameter Tampering,
.env Information Leak, CORS Misconfiguration, JWT / Auth Bypass, HSTS, y más.

---

### Frontend — `converter.levsek.com.mx`

| Resultado | Cantidad |
|-----------|----------|
| PASS      | 63       |
| WARN      | 0        |
| FAIL      | 0        |

**Headers de seguridad activos:**
HSTS, CSP (SHA256), X-Frame-Options, X-Content-Type-Options,
Permissions-Policy, COEP, COOP, CORP, Referrer-Policy, Cache-Control.

---

## Cómo ejecutar las pruebas

**Prerequisito:** Docker Desktop instalado y corriendo.

### Paso 1 — Descargar la imagen de ZAP (solo la primera vez)

Abrir Git Bash y ejecutar:

```bash
docker pull ghcr.io/zaproxy/zaproxy:stable
```

---

### Paso 2 — Scan del backend

```bash
bash "C:/Users/Isaac/Desktop/utez/converter-docs/zap-reports/scan-api.sh"
```

El script:
1. Obtiene el JWT token automáticamente
2. Ejecuta el scan activo (~15 min)
3. Abre el reporte en el navegador

---

### Paso 3 — Scan del frontend

```bash
bash "C:/Users/Isaac/Desktop/utez/converter-docs/zap-reports/scan-web.sh"
```

El script:
1. Ejecuta el scan pasivo (~5 min)
2. Abre el reporte en el navegador

---

### Reportes

```
converter-docs/zap-reports/
├── api-report.html   ← Reporte del backend
├── web-report.html   ← Reporte del frontend
```

---

## Endpoints probados (API)

| Método | Endpoint | Auth |
|--------|----------|------|
| POST | `/auth/register/` | Pública |
| POST | `/auth/login/` | Pública |
| POST | `/auth/refresh/` | Pública |
| GET | `/auth/me/` | JWT |
| GET | `/auth/users/` | Admin |
| GET / PATCH / DELETE | `/auth/users/{id}/` | Admin |
| POST | `/convert/` | JWT |
| GET | `/examples/` | Pública |
| GET | `/history/` | JWT |
| GET / DELETE | `/history/{id}/` | JWT |

---

## Nota sobre cifrado AES-GCM

El backend cifra los bodies con AES-GCM. ZAP no puede inyectar en bodies cifrados —
esto es por diseño y representa una capa adicional de defensa.
Los ataques en headers, URL params y estructura HTTP sí fueron ejecutados.

---

## Herramienta

| Campo | Valor |
|-------|-------|
| Herramienta | OWASP ZAP |
| Imagen Docker | `ghcr.io/zaproxy/zaproxy:stable` |
| Modo API | `zap-api-scan.py` (activo con OpenAPI spec) |
| Modo Web | `zap-baseline.py` (pasivo) |
| Spec | `zap-reports/openapi.yaml` |
| Fecha | 2026-04-04 |
