# Épica: Autenticación y Usuarios

**Proyecto:** Converter  
**Módulo backend:** `accounts`  
**Endpoints:** `/register/`, `/login/`, `/refresh/`, `/me/`

---

## HU-01 — Registro de cuenta

**Como** analista,  
**quiero** registrarme con email y contraseña,  
**para** acceder al sistema de conversión de diagramas.

### Criterios de aceptación
- [ ] El sistema valida que el email sea único
- [ ] La contraseña cumple requisitos mínimos de seguridad
- [ ] Se asigna el rol `analyst` por defecto al nuevo usuario
- [ ] Se retorna un token JWT de acceso y refresh al registrarse exitosamente
- [ ] Se muestra mensaje de error claro si el email ya está registrado

**Prioridad:** Alta  
**Estimación:** 3 pts

---

## HU-02 — Inicio de sesión

**Como** analista o administrador,  
**quiero** iniciar sesión con mi email y contraseña,  
**para** autenticarme y acceder a las funciones del sistema.

### Criterios de aceptación
- [ ] El sistema retorna token de acceso y refresh tras credenciales correctas
- [ ] Se muestra mensaje de error si las credenciales son incorrectas
- [ ] El token de acceso tiene tiempo de expiración definido
- [ ] Al iniciar sesión se redirige según el rol (`admin` → panel admin, `analyst` → upload)

**Prioridad:** Alta  
**Estimación:** 2 pts

---

## HU-03 — Renovación de token JWT

**Como** usuario autenticado,  
**quiero** que mi sesión se renueve automáticamente,  
**para** no tener que volver a iniciar sesión mientras estoy trabajando.

### Criterios de aceptación
- [ ] Los interceptores de Axios renuevan el token de acceso usando el refresh token
- [ ] Si el refresh token expira, se redirige al login automáticamente
- [ ] La renovación es transparente para el usuario

**Prioridad:** Alta  
**Estimación:** 2 pts

---

## HU-04 — Cierre de sesión

**Como** usuario autenticado,  
**quiero** cerrar sesión,  
**para** proteger mi cuenta en equipos compartidos.

### Criterios de aceptación
- [ ] Al cerrar sesión se eliminan los tokens del almacenamiento local
- [ ] Se redirige al login tras cerrar sesión
- [ ] No es posible acceder a rutas protegidas tras cerrar sesión

**Prioridad:** Media  
**Estimación:** 1 pt

---

## HU-05 — Ver perfil propio

**Como** usuario autenticado,  
**quiero** consultar mis datos de perfil,  
**para** verificar mi información y rol asignado en el sistema.

### Criterios de aceptación
- [ ] Se expone el endpoint `/me/` que retorna email, username y rol
- [ ] Solo usuarios autenticados pueden acceder al endpoint
- [ ] La información del perfil es visible en el frontend

**Prioridad:** Baja  
**Estimación:** 1 pt
