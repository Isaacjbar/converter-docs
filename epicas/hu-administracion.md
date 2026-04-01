# Épica: Administración de Usuarios

**Proyecto:** Converter  
**Módulo backend:** `accounts` (vistas admin)  
**Endpoints:** `/users/`, `/users/<id>/`  
**Módulo frontend:** `Admin.jsx`  
**Rol requerido:** `admin`

---

## HU-20 — Ver lista de usuarios registrados

**Como** administrador,  
**quiero** ver un listado de todos los usuarios del sistema,  
**para** tener visibilidad del registro de cuentas y su estado actual.

### Criterios de aceptación
- [ ] El endpoint `/users/` está restringido a usuarios con rol `admin`
- [ ] La lista incluye email, username, rol y estado (activo/inactivo) de cada usuario
- [ ] El frontend muestra la lista en una tabla con paginación o scroll
- [ ] Se muestra mensaje si no hay usuarios registrados

**Prioridad:** Alta  
**Estimación:** 2 pts

---

## HU-21 — Cambiar rol de un usuario

**Como** administrador,  
**quiero** cambiar el rol de un usuario entre `analyst` y `admin`,  
**para** asignar o revocar privilegios de administración según sea necesario.

### Criterios de aceptación
- [ ] El endpoint `/users/<id>/` acepta PATCH para actualizar el campo `role`
- [ ] El cambio de rol está restringido a usuarios con rol `admin`
- [ ] El frontend muestra un selector de rol editable por fila en la tabla
- [ ] El cambio se refleja en la interfaz inmediatamente tras guardar

**Prioridad:** Alta  
**Estimación:** 2 pts

---

## HU-22 — Activar o desactivar un usuario

**Como** administrador,  
**quiero** activar o desactivar la cuenta de un usuario,  
**para** controlar el acceso al sistema sin necesidad de eliminar la cuenta.

### Criterios de aceptación
- [ ] El endpoint `/users/<id>/` acepta PATCH para actualizar el campo `is_active`
- [ ] Un usuario desactivado no puede iniciar sesión
- [ ] El frontend muestra un toggle o botón de estado activo/inactivo por usuario
- [ ] Se solicita confirmación antes de desactivar una cuenta

**Prioridad:** Alta  
**Estimación:** 2 pts

---

## HU-23 — Ver detalle de un usuario

**Como** administrador,  
**quiero** ver el detalle completo de un usuario específico,  
**para** revisar su información, rol y actividad antes de tomar decisiones administrativas.

### Criterios de aceptación
- [ ] El endpoint `/users/<id>/` retorna todos los campos del usuario
- [ ] Solo usuarios con rol `admin` pueden acceder al detalle
- [ ] El frontend permite navegar al detalle desde la tabla de usuarios

**Prioridad:** Media  
**Estimación:** 1 pt
