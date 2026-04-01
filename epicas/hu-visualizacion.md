# Épica: Visualización de Diagramas

**Proyecto:** Converter  
**Módulo frontend:** `DiagramView.jsx`, `PlantUMLRenderer`  
**Relacionado con:** `/convert/`

---

## HU-12 — Ver diagrama generado en SVG

**Como** analista,  
**quiero** ver el diagrama UML generado renderizado como imagen SVG,  
**para** visualizarlo directamente en el navegador sin descargar archivos.

### Criterios de aceptación
- [ ] El frontend comprime el código PlantUML con `pako` y construye la URL del servidor PlantUML
- [ ] El diagrama se muestra como imagen SVG incrustada en la página
- [ ] Si el diagrama no se puede renderizar se muestra un mensaje de error claro
- [ ] El SVG se ajusta al ancho del contenedor

**Prioridad:** Alta  
**Estimación:** 3 pts

---

## HU-13 — Navegar entre tipos de diagrama por pestañas

**Como** analista,  
**quiero** cambiar entre diagrama de clases, casos de uso y flujo mediante pestañas,  
**para** revisar los tres diagramas generados de una misma conversión sin recargar.

### Criterios de aceptación
- [ ] La vista muestra tres pestañas: Clases, Casos de Uso, Flujo
- [ ] Al cambiar de pestaña se renderiza el diagrama correspondiente
- [ ] La pestaña activa se indica visualmente
- [ ] Si un tipo de diagrama no fue generado la pestaña se deshabilita o muestra aviso

**Prioridad:** Alta  
**Estimación:** 2 pts

---

## HU-14 — Imprimir diagrama

**Como** analista,  
**quiero** imprimir el diagrama que estoy viendo,  
**para** incluirlo en documentación física o exportarlo como PDF desde el navegador.

### Criterios de aceptación
- [ ] Existe un botón "Imprimir" en la vista de diagrama
- [ ] Al imprimir solo se muestra el diagrama activo, sin navegación ni header
- [ ] El layout de impresión está optimizado mediante `print.css`

**Prioridad:** Media  
**Estimación:** 1 pt

---

## HU-15 — Cambiar tema oscuro/claro

**Como** analista,  
**quiero** alternar entre tema oscuro y claro en la interfaz,  
**para** adaptar la visualización a mis preferencias o condiciones de luz.

### Criterios de aceptación
- [ ] La Navbar incluye un toggle de tema oscuro/claro
- [ ] El tema seleccionado se aplica globalmente a toda la interfaz
- [ ] La preferencia de tema persiste al navegar entre páginas

**Prioridad:** Baja  
**Estimación:** 1 pt
