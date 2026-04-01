# Requisitos de Base de Datos

**Proyecto:** Converter  
**Asignatura:** Bases de Datos  
**Estado:** Pendiente de implementación — este documento sirve como referencia de diseño.

> Nota: El proyecto actualmente usa SQLite para desarrollo local. Los eventos programados y triggers nativos descritos en este documento requieren un motor como **MySQL 8+** o **PostgreSQL 14+**. Se deberá migrar la configuración de `DATABASES` en `settings.py` previo a su implementación.

---

## Eventos Programados

Se deberán implementar al menos **dos eventos programados** con función real dentro del sistema.

### Evento 1 — Limpieza de historial antiguo

**Nombre:** `evt_purge_old_history`  
**Frecuencia:** Cada semana (domingos a las 02:00)  
**Función:** Eliminar registros de `DiagramHistory` con más de 90 días de antigüedad para evitar el crecimiento indefinido de la base de datos.

```sql
CREATE EVENT evt_purge_old_history
ON SCHEDULE EVERY 1 WEEK
STARTS '2026-04-06 02:00:00'
DO
  DELETE FROM history_diagramhistory
  WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
```

---

### Evento 2 — Desactivación de usuarios inactivos

**Nombre:** `evt_deactivate_inactive_users`  
**Frecuencia:** Cada mes (primer día del mes a las 03:00)  
**Función:** Desactivar automáticamente cuentas de usuarios que no hayan generado ninguna conversión en los últimos 60 días, estableciendo `is_active = 0`.

```sql
CREATE EVENT evt_deactivate_inactive_users
ON SCHEDULE EVERY 1 MONTH
STARTS '2026-05-01 03:00:00'
DO
  UPDATE accounts_user
  SET is_active = 0
  WHERE id NOT IN (
    SELECT DISTINCT user_id FROM history_diagramhistory
    WHERE created_at >= DATE_SUB(NOW(), INTERVAL 60 DAY)
  )
  AND is_superuser = 0;
```

---

## Triggers

Se deberán implementar al menos **dos triggers funcionales** que respondan a operaciones relevantes del sistema.

### Trigger 1 — Auditoría de cambios de rol

**Nombre:** `trg_audit_role_change`  
**Evento:** `AFTER UPDATE` en `accounts_user`  
**Función:** Registrar en una tabla de auditoría cualquier cambio de rol de usuario, guardando el valor anterior, el nuevo valor, la fecha y el usuario que fue modificado.

```sql
CREATE TABLE audit_role_changes (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  user_id     INT NOT NULL,
  old_role    VARCHAR(10),
  new_role    VARCHAR(10),
  changed_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_audit_role_change
AFTER UPDATE ON accounts_user
FOR EACH ROW
BEGIN
  IF OLD.role <> NEW.role THEN
    INSERT INTO audit_role_changes (user_id, old_role, new_role)
    VALUES (OLD.id, OLD.role, NEW.role);
  END IF;
END;
```

---

### Trigger 2 — Control de versión antes de insertar historial

**Nombre:** `trg_set_diagram_version`  
**Evento:** `BEFORE INSERT` en `history_diagramhistory`  
**Función:** Calcular automáticamente el número de versión de un diagrama antes de insertarlo, basándose en el conteo de registros existentes con el mismo `user_id` y `filename`.

```sql
CREATE TRIGGER trg_set_diagram_version
BEFORE INSERT ON history_diagramhistory
FOR EACH ROW
BEGIN
  DECLARE max_ver INT;
  SELECT COALESCE(MAX(version), 0)
    INTO max_ver
    FROM history_diagramhistory
   WHERE user_id = NEW.user_id
     AND filename = NEW.filename;
  SET NEW.version = max_ver + 1;
END;
```

---

## Vistas

Se deberán implementar al menos **dos vistas** para simplificar consultas, restringir acceso o apoyar reportes.

### Vista 1 — Resumen de actividad por usuario

**Nombre:** `vw_user_activity_summary`  
**Función:** Proveer un resumen del número de conversiones realizadas por cada usuario, útil para reportes de administración.

```sql
CREATE VIEW vw_user_activity_summary AS
SELECT
  u.id                        AS user_id,
  u.email,
  u.role,
  u.is_active,
  COUNT(h.id)                 AS total_conversions,
  MAX(h.created_at)           AS last_conversion_at
FROM accounts_user u
LEFT JOIN history_diagramhistory h ON h.user_id = u.id
GROUP BY u.id, u.email, u.role, u.is_active;
```

**Uso:** Consultada desde el panel de administración para listar usuarios con métricas de uso.

---

### Vista 2 — Historial reciente de conversiones (últimos 30 días)

**Nombre:** `vw_recent_conversions`  
**Función:** Exponer solo las conversiones de los últimos 30 días para simplificar consultas frecuentes del dashboard y evitar escaneo completo de la tabla.

```sql
CREATE VIEW vw_recent_conversions AS
SELECT
  h.id,
  h.filename,
  h.version,
  h.created_at,
  u.email    AS user_email,
  u.role     AS user_role
FROM history_diagramhistory h
INNER JOIN accounts_user u ON u.id = h.user_id
WHERE h.created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY);
```

**Uso:** Consultada en reportes de actividad reciente y estadísticas del sistema.

---

## Índices

Los índices se colocarán **únicamente sobre datos críticos identificados** en los modelos del sistema. Queda prohibido crear índices de manera indiscriminada.

### Datos críticos identificados

| Tabla | Campo | Tipo de índice | Justificación |
|---|---|---|---|
| `accounts_user` | `email` | Único | Campo de autenticación principal, consultado en cada login |
| `history_diagramhistory` | `user_id` | Simple | Clave foránea consultada en cada listado de historial por usuario |
| `history_diagramhistory` | `(user_id, filename)` | Compuesto | Consultado en cada inserción para calcular el versionado automático |
| `history_diagramhistory` | `created_at` | Simple | Usado en ordenamiento por fecha y en el evento de limpieza periódica |

```sql
-- Índice único sobre email (Django lo genera automáticamente por unique=True)
CREATE UNIQUE INDEX idx_user_email ON accounts_user(email);

-- Índice simple sobre user_id en historial
CREATE INDEX idx_history_user ON history_diagramhistory(user_id);

-- Índice compuesto para versionado por archivo
CREATE INDEX idx_history_user_filename ON history_diagramhistory(user_id, filename);

-- Índice simple sobre fecha de creación
CREATE INDEX idx_history_created ON history_diagramhistory(created_at);
```

---

## Base de Datos Poblada con Registros de Prueba

La base de datos deberá contener registros reales de prueba que permitan validar el funcionamiento del sistema. Ver sección **"Poblar la base de datos"** en el [`README.md`](../README.md) para los comandos exactos.

### Registros mínimos requeridos

| Tabla | Registros mínimos | Descripción |
|---|---|---|
| `accounts_user` | 5+ | Al menos 1 admin y 4 analistas |
| `history_diagramhistory` | 10+ | Al menos 3 archivos distintos con múltiples versiones |

---

## Reporte de Avances y Copias de Seguridad

### Reporte de avances

El equipo deberá entregar un reporte que incluya:

- Descripción de los avances realizados en la asignatura
- Capturas de pantalla de la base de datos poblada
- Evidencia de ejecución de triggers y eventos programados
- Evidencia de consultas sobre las vistas implementadas
- Listado de índices creados con justificación

### Copias de seguridad

Se deberá entregar evidencia de la creación de copias de seguridad de la base de datos de acuerdo con el tipo de respaldo que el equipo haya establecido.

#### Tipos de respaldo a considerar

| Tipo | Descripción | Comando de referencia (MySQL) |
|---|---|---|
| **Completa** | Exportación total de la base de datos | `mysqldump -u root -p converter_db > backup_completo_YYYY-MM-DD.sql` |
| **Incremental** | Solo cambios desde el último respaldo | Requiere activar binary log en MySQL (`binlog`) |
| **Diferencial** | Cambios desde el último respaldo completo | Basado en binary log desde el punto del backup completo |

#### Respaldo completo recomendado para desarrollo

```bash
# MySQL
mysqldump -u root -p converter_db > backups/backup_completo_$(date +%F).sql

# SQLite (entorno de desarrollo)
cp db.sqlite3 backups/db_backup_$(date +%F).sqlite3
```

La evidencia de los respaldos deberá incluir:
- [ ] Archivo(s) de respaldo generados con fecha en el nombre
- [ ] Captura de pantalla del proceso de generación
- [ ] Captura de pantalla de la restauración exitosa del respaldo
