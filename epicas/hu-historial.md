# Épica: Historial de Conversiones

**Proyecto:** Converter  
**Módulo backend:** `history`  
**Endpoints:** `/history/`, `/history/<id>/`  
**Modelo:** `DiagramHistory`

---

## HU-16 — Ver lista de conversiones previas

**Como** analista,  
**quiero** ver un listado de todas mis conversiones anteriores,  
**para** acceder rápidamente a diagramas que ya generé sin tener que volver a subir el archivo.

### Criterios de aceptación
- [ ] El endpoint `/history/` retorna solo las conversiones del usuario autenticado
- [ ] Cada entrada muestra nombre de archivo, versión y fecha de creación
- [ ] La lista está ordenada de más reciente a más antigua
- [ ] Se muestra mensaje si el historial está vacío

**Prioridad:** Alta  
**Estimación:** 2 pts

---

## HU-17 — Ver detalle de una conversión

**Como** analista,  
**quiero** ver el detalle completo de una conversión pasada,  
**para** revisar el código fuente original y los diagramas generados en esa sesión.

### Criterios de aceptación
- [ ] El endpoint `/history/<id>/` retorna código fuente, los tres diagramas y metadatos
- [ ] Solo el propietario del registro puede acceder al detalle
- [ ] Los diagramas se renderizan en la vista de detalle igual que en la vista principal
- [ ] Se muestra la versión del archivo en el detalle

**Prioridad:** Alta  
**Estimación:** 2 pts

---

## HU-18 — Eliminar conversión del historial

**Como** analista,  
**quiero** eliminar una conversión de mi historial,  
**para** mantener mi historial organizado y libre de entradas innecesarias.

### Criterios de aceptación
- [ ] Existe un botón de eliminar en la vista de historial y/o detalle
- [ ] Se solicita confirmación antes de eliminar
- [ ] Solo el propietario del registro puede eliminarlo
- [ ] Tras eliminar se actualiza la lista sin recargar la página

**Prioridad:** Media  
**Estimación:** 2 pts

---

## HU-19 — Versionado automático de conversiones

**Como** analista,  
**quiero** que el sistema versione automáticamente cuando convierto el mismo archivo más de una vez,  
**para** llevar un registro de la evolución del código sin sobrescribir conversiones anteriores.

### Criterios de aceptación
- [ ] Al convertir un archivo con el mismo nombre, se crea una nueva entrada con versión incrementada (v1, v2, v3…)
- [ ] Todas las versiones del mismo archivo son visibles en el historial
- [ ] La versión se muestra claramente en la lista y el detalle
- [ ] El versionado es por usuario y por nombre de archivo

**Prioridad:** Media  
**Estimación:** 3 pts
