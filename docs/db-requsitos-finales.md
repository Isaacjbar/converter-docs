```markdown
# SEGUNDO AVANCE PROYECTO INTEGRADOR: REPORTE DE MONITOREO DE BASE DE DATOS

## Objetivo
Evaluar el rendimiento de la base de datos utilizada en el sistema desarrollado con Django y MySQL, mediante el monitoreo de diversas métricas clave para identificar cuellos de botella, errores y oportunidades de mejora.

---

## Instrucciones

1. Todos los integrantes del equipo deberán conectarse simultáneamente al sistema y realizar diversas peticiones (consultas, inserciones, actualizaciones, etc.) para generar carga sobre la base de datos.
2. Durante este periodo, se deben recopilar las métricas indicadas utilizando herramientas como:
   - Grafana
   - Prometheus
   - mysqld_exporter
3. Se deben anexar capturas de pantalla como evidencia de cada una de las actividades realizadas durante el monitoreo.
4. Investigar para qué sirve cada una de las métricas monitoreadas.
5. El reporte debe estar en formato PDF e incluir los datos obtenidos, su interpretación y posibles acciones de mejora.

---

## Métricas a monitorear

1. `mysql_up`
2. `rate(mysql_global_status_queries[1m])`
3. ```sql
   SELECT
     ROUND(SUM(SUM_TIMER_WAIT) / SUM(COUNT_STAR) / 1000000000000, 6) AS avg_response_time_sec
   FROM performance_schema.events_statements_summary_by_digest
   WHERE COUNT_STAR > 0;
   ```
4. `mysql_global_status_slow_queries`
5. `mysql_global_status_threads_connected`
6. `mysql_global_status_aborted_connects`
7. `mysql_global_status_connections`
8. `(1 - (rate(mysql_global_status_innodb_buffer_pool_reads[5m]) / rate(mysql_global_status_innodb_buffer_pool_read_requests[5m]))) * 100`
9. `rate(mysql_global_status_innodb_pages_written[5m])`
10. `(rate(mysql_global_status_select_scan[5m]) / rate(mysql_global_status_questions[5m])) * 100`
11. `mysql_global_status_connection_errors_total`
12. ```sql
    SELECT TABLE_SCHEMA, TABLE_NAME, DATA_FREE
    FROM information_schema.tables
    WHERE DATA_FREE > 0
    ORDER BY DATA_FREE DESC;
    ```
13. `mysql_global_status_innodb_deadlocks`

---

## Contenido del reporte

- **Portada** con nombre del proyecto, integrantes del equipo, fecha y grupo.
- **Breve descripción** de cómo realizaron el monitoreo.
- **Tabla** con las métricas, valores obtenidos, análisis e interpretación.
- **Acciones de mejora** sugeridas.
- **Evidencia** en forma de capturas de pantalla o consultas ejecutadas.
```