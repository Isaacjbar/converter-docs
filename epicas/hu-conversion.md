# Épica: Conversión de Código Java

**Proyecto:** Converter  
**Módulo backend:** `converter`, `parsers`, `diagrams`  
**Endpoints:** `/convert/`, `/examples/`

---

## HU-06 — Subir archivo Java para conversión

**Como** analista,  
**quiero** subir un archivo `.java` mediante drag-drop o selector de archivos,  
**para** convertirlo automáticamente a diagramas UML.

### Criterios de aceptación
- [ ] El componente acepta archivos `.java` por arrastre o selección
- [ ] Se valida que el archivo tenga extensión `.java`
- [ ] Se muestra indicador de carga durante el procesamiento
- [ ] Se muestra mensaje de error si el archivo no es válido

**Prioridad:** Alta  
**Estimación:** 3 pts

---

## HU-07 — Pegar código Java directamente

**Como** analista,  
**quiero** pegar código Java en un editor de texto,  
**para** convertirlo sin necesidad de crear un archivo.

### Criterios de aceptación
- [ ] La página Upload ofrece un área de texto para pegar código
- [ ] El usuario puede alternar entre subir archivo y pegar código
- [ ] Se valida que el contenido no esté vacío antes de enviar
- [ ] Se muestra mensaje de error si el código no es Java válido

**Prioridad:** Alta  
**Estimación:** 2 pts

---

## HU-08 — Generar diagrama de clases

**Como** analista,  
**quiero** obtener un diagrama de clases a partir de mi código Java,  
**para** visualizar la estructura de clases, atributos, métodos y relaciones de herencia.

### Criterios de aceptación
- [ ] El parser extrae clases, campos, métodos e interfaces del AST de Java
- [ ] El generador produce código PlantUML válido para diagrama de clases
- [ ] Se representan correctamente las relaciones de herencia y asociación
- [ ] El diagrama se renderiza como SVG en el frontend

**Prioridad:** Alta  
**Estimación:** 5 pts

---

## HU-09 — Generar diagrama de casos de uso

**Como** analista,  
**quiero** obtener un diagrama de casos de uso a partir de mi código Java,  
**para** identificar los actores y funcionalidades del sistema.

### Criterios de aceptación
- [ ] El generador infiere actores y casos de uso mediante heurísticas sobre el AST
- [ ] El diagrama de casos de uso se incluye en la respuesta de la API
- [ ] El diagrama se renderiza correctamente en el frontend

**Prioridad:** Alta  
**Estimación:** 5 pts

---

## HU-10 — Generar diagrama de flujo

**Como** analista,  
**quiero** obtener un diagrama de flujo de control a partir de mi código Java,  
**para** entender la lógica de ejecución del programa.

### Criterios de aceptación
- [ ] El generador analiza estructuras de control (if, for, while, switch) del AST
- [ ] El diagrama de flujo se incluye en la respuesta de la API
- [ ] El diagrama se renderiza correctamente en el frontend

**Prioridad:** Alta  
**Estimación:** 5 pts

---

## HU-11 — Ver ejemplos de conversión

**Como** analista nuevo,  
**quiero** consultar ejemplos de conversiones predefinidas,  
**para** entender qué tipo de código Java acepta el sistema y qué diagramas genera.

### Criterios de aceptación
- [ ] El endpoint `/examples/` retorna al menos un ejemplo de código Java con sus diagramas
- [ ] Los ejemplos son accesibles sin necesidad de autenticación (o con, según política)
- [ ] Los ejemplos se muestran de forma clara en el frontend

**Prioridad:** Baja  
**Estimación:** 2 pts
