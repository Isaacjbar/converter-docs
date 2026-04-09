import base64

def img_b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

dash = img_b64('C:/Users/Isaac/Desktop/utez/dashboard-mysql-2.png')
targets = img_b64('C:/Users/Isaac/Desktop/utez/prometheus-targets.png')

html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', Arial, sans-serif; color: #1a1a1a; background: #fff; font-size: 13px; }
  .cover { display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 100vh; background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 100%); color: white; text-align: center; padding: 40px; page-break-after: always; }
  .cover h1 { font-size: 26px; font-weight: 700; margin-bottom: 10px; }
  .cover h2 { font-size: 18px; font-weight: 400; margin-bottom: 40px; opacity: 0.85; }
  .cover .badge { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); border-radius: 8px; padding: 20px 40px; margin-bottom: 40px; }
  .cover .badge h3 { font-size: 13px; opacity: 0.7; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 2px; }
  .cover .badge p { font-size: 15px; line-height: 2; }
  .cover .meta { font-size: 13px; opacity: 0.7; }
  .cover .meta span { display: block; margin: 4px 0; }
  .page { padding: 40px 50px; max-width: 900px; margin: 0 auto; }
  h2.section { font-size: 18px; color: #1e3a5f; border-bottom: 3px solid #2d6a9f; padding-bottom: 8px; margin: 30px 0 16px; }
  p { line-height: 1.7; margin-bottom: 10px; color: #333; }
  .metric-card { border: 1px solid #e0e7ef; border-radius: 8px; padding: 16px 20px; margin: 12px 0; background: #f8fbff; }
  .metric-card .header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
  .metric-card .name { font-weight: 700; color: #1e3a5f; font-size: 13px; }
  .metric-card .value-ok { font-size: 16px; font-weight: 700; color: #16a34a; background: #dcfce7; padding: 4px 12px; border-radius: 20px; white-space: nowrap; }
  .metric-card .value-warn { font-size: 16px; font-weight: 700; color: #d97706; background: #fef9c3; padding: 4px 12px; border-radius: 20px; white-space: nowrap; }
  .metric-card .value-info { font-size: 16px; font-weight: 700; color: #2563eb; background: #dbeafe; padding: 4px 12px; border-radius: 20px; white-space: nowrap; }
  .metric-card .query { font-family: monospace; font-size: 11px; background: #1e1e2e; color: #cdd6f4; padding: 8px 12px; border-radius: 6px; margin: 8px 0; white-space: pre-wrap; word-break: break-all; }
  .metric-card .desc { color: #555; font-size: 12px; line-height: 1.6; }
  .img-block { margin: 20px 0; text-align: center; }
  .img-block img { max-width: 100%; border-radius: 8px; border: 1px solid #ddd; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
  .img-block .caption { font-size: 11px; color: #888; margin-top: 6px; font-style: italic; }
  table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 12px; }
  th { background: #1e3a5f; color: white; padding: 10px 12px; text-align: left; }
  td { padding: 9px 12px; border-bottom: 1px solid #e5e7eb; }
  tr:nth-child(even) td { background: #f8fbff; }
  .mejora { background: #f0fdf4; border-left: 4px solid #16a34a; padding: 12px 16px; margin: 10px 0; border-radius: 0 6px 6px 0; }
  .mejora strong { color: #15803d; display: block; margin-bottom: 6px; }
  .page-break { page-break-before: always; }
  code { font-family: monospace; background: #f1f5f9; padding: 2px 6px; border-radius: 3px; font-size: 11px; }
</style>
</head>
<body>

<div class="cover">
  <h1>Reporte de Monitoreo de Base de Datos</h1>
  <h2>Segundo Avance &mdash; Proyecto Integrador</h2>
  <div class="badge">
    <h3>Equipo</h3>
    <p>
      Apaez Sotelo Alexis Jesus<br>
      Canchola Aguilar Alan Yahir<br>
      Jimenez Barcelata Isaac<br>
      Negrete Ju&aacute;rez Vanessa<br>
      P&eacute;rez Bosques Laura Lizet<br>
      Ram&iacute;rez L&oacute;pez Alicia Fernanda
    </p>
  </div>
  <div class="meta">
    <span>Materia: Administraci&oacute;n de Bases de Datos</span>
    <span>Sistema: service-converter (Django + MySQL)</span>
    <span>Fecha: 9 de abril de 2026</span>
  </div>
</div>

<div class="page">
  <h2 class="section">&iquest;C&oacute;mo hicimos el monitoreo?</h2>
  <p>Para este reporte conectamos tres herramientas que trabajan juntas: <strong>mysqld_exporter</strong> se encarga de leer el estado interno de MySQL y exponer esa informaci&oacute;n como m&eacute;tricas, <strong>Prometheus</strong> recoge esas m&eacute;tricas cada 15 segundos y las guarda, y <strong>Grafana</strong> las muestra de forma visual en tiempo real.</p>
  <p>La base de datos monitoreada es <code>converter_db</code>, alojada en el servidor <code>158.69.218.237:3350</code>. Durante la sesi&oacute;n generamos carga realizando inserciones, consultas y actualizaciones sobre la tabla <code>history_diagramhistory</code> para que las m&eacute;tricas reflejaran actividad real.</p>

  <h2 class="section">Herramientas utilizadas</h2>
  <table>
    <tr><th>Herramienta</th><th>Versi&oacute;n</th><th>Puerto</th><th>Funci&oacute;n</th></tr>
    <tr><td>mysqld_exporter</td><td>0.16.0</td><td>9104</td><td>Extrae m&eacute;tricas de MySQL y las expone en /metrics</td></tr>
    <tr><td>Prometheus</td><td>3.5.1</td><td>9090</td><td>Recolecta y almacena las m&eacute;tricas en series de tiempo</td></tr>
    <tr><td>Grafana</td><td>12.3.2</td><td>3000</td><td>Visualiza las m&eacute;tricas mediante paneles y dashboards</td></tr>
  </table>

  <div class="img-block">
    <img src="data:image/png;base64,""" + targets + """" alt="Prometheus targets">
    <div class="caption">Figura 1 &mdash; Prometheus targets: mysql_converter en estado UP</div>
  </div>

  <div class="img-block">
    <img src="data:image/png;base64,""" + dash + """" alt="Dashboard Grafana">
    <div class="caption">Figura 2 &mdash; Dashboard de monitoreo MySQL en Grafana</div>
  </div>
</div>

<div class="page page-break">
  <h2 class="section">M&eacute;tricas monitoreadas</h2>

  <div class="metric-card">
    <div class="header">
      <div class="name">1. Estado del servidor MySQL</div>
      <div class="value-ok">UP &mdash; 1</div>
    </div>
    <div class="query">mysql_up</div>
    <div class="desc">Indica si el servidor MySQL est&aacute; disponible. El valor <strong>1</strong> significa que est&aacute; funcionando correctamente; <strong>0</strong> indicar&iacute;a que est&aacute; ca&iacute;do. Es la m&eacute;trica m&aacute;s b&aacute;sica y fundamental: si esto falla, todo lo dem&aacute;s tambi&eacute;n falla.</div>
  </div>

  <div class="metric-card">
    <div class="header">
      <div class="name">2. Tasa de consultas por segundo</div>
      <div class="value-info">1.37 q/s</div>
    </div>
    <div class="query">rate(mysql_global_status_queries[1m])</div>
    <div class="desc">Mide cu&aacute;ntas consultas se ejecutan por segundo en el &uacute;ltimo minuto. Un valor de <strong>1.37 consultas/seg</strong> es bajo y saludable para desarrollo. En producci&oacute;n bajo carga alta puede llegar a cientos; si sube de golpe sin raz&oacute;n aparente puede indicar un problema.</div>
  </div>

  <div class="metric-card">
    <div class="header">
      <div class="name">3. Tiempo promedio de respuesta por consulta</div>
      <div class="value-info">N/A</div>
    </div>
    <div class="query">SELECT ROUND(SUM(SUM_TIMER_WAIT)/SUM(COUNT_STAR)/1000000000000,6) AS avg_response_time_sec
FROM performance_schema.events_statements_summary_by_digest
WHERE COUNT_STAR &gt; 0;</div>
    <div class="desc">Esta consulta calcula cu&aacute;nto tarda en promedio cada instrucci&oacute;n SQL. El usuario <code>converter_user</code> no tiene permisos sobre <code>performance_schema</code>, por lo que no fue posible obtener el valor. Para habilitarlo se necesitar&iacute;a <code>GRANT SELECT ON performance_schema.* TO 'converter_user'@'%'</code>. Tiempos menores a 0.01 seg son excelentes; mayores a 1 seg indican cuellos de botella.</div>
  </div>

  <div class="metric-card">
    <div class="header">
      <div class="name">4. Consultas lentas acumuladas</div>
      <div class="value-ok">0</div>
    </div>
    <div class="query">mysql_global_status_slow_queries</div>
    <div class="desc">Cuenta las consultas que tardaron m&aacute;s del umbral configurado en <code>long_query_time</code>. Que sea <strong>0</strong> es excelente: ninguna consulta ha tardado demasiado. Si empezara a subir ser&iacute;a se&ntilde;al de queries mal optimizados o &iacute;ndices faltantes.</div>
  </div>

  <div class="metric-card">
    <div class="header">
      <div class="name">5. Hilos conectados actualmente</div>
      <div class="value-warn">30</div>
    </div>
    <div class="query">mysql_global_status_threads_connected</div>
    <div class="desc">Muestra cu&aacute;ntas conexiones activas hay abiertas con MySQL en este momento. <strong>30 hilos</strong> es moderado y normal. Este n&uacute;mero se debe comparar con el l&iacute;mite <code>max_connections</code>; si se acerca al l&iacute;mite, nuevas conexiones ser&aacute;n rechazadas.</div>
  </div>

  <div class="metric-card">
    <div class="header">
      <div class="name">6. Intentos de conexi&oacute;n abortados</div>
      <div class="value-ok">0</div>
    </div>
    <div class="query">mysql_global_status_aborted_connects</div>
    <div class="desc">Registra cu&aacute;ntas veces un cliente intent&oacute; conectarse pero fall&oacute; antes de completar la autenticaci&oacute;n. Un valor de <strong>0</strong> significa que no ha habido credenciales incorrectas, timeouts ni errores de configuraci&oacute;n. Si creciera podr&iacute;a indicar un ataque o mala configuraci&oacute;n en alguna app.</div>
  </div>

  <div class="metric-card">
    <div class="header">
      <div class="name">7. Conexiones totales desde el inicio</div>
      <div class="value-info">1,297</div>
    </div>
    <div class="query">mysql_global_status_connections</div>
    <div class="desc">Contador acumulado de todas las conexiones establecidas desde que el servidor arranc&oacute;. Con <strong>1,297 conexiones</strong> y el sistema relativamente reciente, indica un uso moderado y continuo. Lo importante es monitorear su tasa de crecimiento en el tiempo.</div>
  </div>

  <div class="metric-card">
    <div class="header">
      <div class="name">8. Eficiencia del buffer pool de InnoDB</div>
      <div class="value-ok">100%</div>
    </div>
    <div class="query">(1 - (rate(mysql_global_status_innodb_buffer_pool_reads[5m]) /
     rate(mysql_global_status_innodb_buffer_pool_read_requests[5m]))) * 100</div>
    <div class="desc">Mide qu&eacute; porcentaje de lecturas se sirven desde RAM en lugar del disco. Un <strong>100%</strong> significa que toda la data est&aacute; cargada en memoria, resultando en lecturas ultrarrápidas. Valores bajo el 90% indicar&iacute;an que el buffer pool es muy peque&ntilde;o para los datos que se trabajan.</div>
  </div>

  <div class="metric-card">
    <div class="header">
      <div class="name">9. P&aacute;ginas InnoDB escritas por segundo</div>
      <div class="value-ok">0.0235 p&aacute;g/s</div>
    </div>
    <div class="query">rate(mysql_global_status_innodb_pages_written[5m])</div>
    <div class="desc">Indica la velocidad a la que InnoDB escribe p&aacute;ginas de datos al disco. Un ritmo de <strong>0.0235 p&aacute;ginas/seg</strong> es muy bajo, normal para poca carga de escritura. Valores muy altos pueden indicar una carga intensiva que podr&iacute;a saturar el disco.</div>
  </div>

  <div class="metric-card">
    <div class="header">
      <div class="name">10. Porcentaje de full table scans</div>
      <div class="value-warn">59%</div>
    </div>
    <div class="query">(rate(mysql_global_status_select_scan[5m]) /
 rate(mysql_global_status_questions[5m])) * 100</div>
    <div class="desc">Muestra qu&eacute; porcentaje de los SELECT recorren tablas completas sin usar &iacute;ndices. Un <strong>59%</strong> es alto &mdash; idealmente deber&iacute;a estar bajo el 20%. Esto sugiere que varias consultas no aprovechan &iacute;ndices, lo que se vuelve costoso conforme las tablas crecen.</div>
  </div>

  <div class="metric-card">
    <div class="header">
      <div class="name">11. Errores totales de conexi&oacute;n</div>
      <div class="value-ok">0</div>
    </div>
    <div class="query">mysql_global_status_connection_errors_total</div>
    <div class="desc">Acumula todos los errores que ocurrieron durante el proceso de conexi&oacute;n. El valor <strong>0</strong> confirma que la conectividad entre la aplicaci&oacute;n y la base de datos ha sido perfecta durante todo el periodo monitoreado.</div>
  </div>

  <div class="metric-card">
    <div class="header">
      <div class="name">12. Fragmentaci&oacute;n de tablas</div>
      <div class="value-ok">Sin fragmentaci&oacute;n</div>
    </div>
    <div class="query">SELECT TABLE_SCHEMA, TABLE_NAME, DATA_FREE
FROM information_schema.tables
WHERE DATA_FREE &gt; 0
ORDER BY DATA_FREE DESC;</div>
    <div class="desc">Muestra qu&eacute; tablas tienen espacio fragmentado producto de eliminaciones o actualizaciones frecuentes. El resultado vac&iacute;o indica que <strong>ninguna tabla tiene fragmentaci&oacute;n</strong>, lo cual es excelente. La fragmentaci&oacute;n reduce el rendimiento y desperdicia espacio en disco.</div>
  </div>

  <div class="metric-card">
    <div class="header">
      <div class="name">13. Deadlocks en InnoDB</div>
      <div class="value-ok">0</div>
    </div>
    <div class="query">mysql_global_status_innodb_deadlocks</div>
    <div class="desc">Cuenta los bloqueos mutuos entre transacciones. Un deadlock ocurre cuando dos operaciones se bloquean entre s&iacute; esperando recursos que la otra tiene reservados. El valor <strong>0</strong> indica que no ha habido ning&uacute;n conflicto, normal en un sistema con baja concurrencia.</div>
  </div>
</div>

<div class="page page-break">
  <h2 class="section">Resumen de resultados</h2>
  <table>
    <tr><th>#</th><th>M&eacute;trica</th><th>Valor obtenido</th><th>Interpretaci&oacute;n</th></tr>
    <tr><td>1</td><td>mysql_up</td><td>1 (UP)</td><td>Servidor en l&iacute;nea y funcionando</td></tr>
    <tr><td>2</td><td>Queries por segundo</td><td>1.37 q/s</td><td>Carga baja, sistema saludable</td></tr>
    <tr><td>3</td><td>Tiempo prom. respuesta</td><td>N/A</td><td>Sin permisos en performance_schema</td></tr>
    <tr><td>4</td><td>Slow queries</td><td>0</td><td>Ninguna consulta lenta registrada</td></tr>
    <tr><td>5</td><td>Threads conectados</td><td>30</td><td>Conexiones activas moderadas</td></tr>
    <tr><td>6</td><td>Conexiones abortadas</td><td>0</td><td>Sin intentos fallidos de autenticaci&oacute;n</td></tr>
    <tr><td>7</td><td>Conexiones totales</td><td>1,297</td><td>Uso continuo desde inicio del servicio</td></tr>
    <tr><td>8</td><td>Buffer pool hit rate</td><td>100%</td><td>Toda la data se lee desde RAM, &oacute;ptimo</td></tr>
    <tr><td>9</td><td>P&aacute;ginas InnoDB escritas/s</td><td>0.0235</td><td>Carga de escritura muy baja</td></tr>
    <tr><td>10</td><td>Full table scans</td><td>59%</td><td>Alto &mdash; requiere revisi&oacute;n de &iacute;ndices</td></tr>
    <tr><td>11</td><td>Errores de conexi&oacute;n</td><td>0</td><td>Conectividad perfecta</td></tr>
    <tr><td>12</td><td>Fragmentaci&oacute;n de tablas</td><td>Sin fragmentaci&oacute;n</td><td>Tablas en buen estado</td></tr>
    <tr><td>13</td><td>Deadlocks InnoDB</td><td>0</td><td>Sin conflictos de transacciones</td></tr>
  </table>

  <h2 class="section">Acciones de mejora sugeridas</h2>

  <div class="mejora">
    <strong>Revisar y agregar &iacute;ndices (prioridad alta)</strong>
    El 59% de full table scans es la se&ntilde;al m&aacute;s preocupante del reporte. Habr&iacute;a que analizar qu&eacute; columnas se usan en cl&aacute;usulas WHERE, JOIN y ORDER BY y crear &iacute;ndices en ellas, especialmente en <code>history_diagramhistory.user_id</code> y <code>history_diagramhistory.created_at</code>, que son las m&aacute;s consultadas.
  </div>

  <div class="mejora">
    <strong>Otorgar acceso a performance_schema</strong>
    Para medir el tiempo promedio de respuesta (m&eacute;trica 3) se necesita ejecutar: <code>GRANT SELECT ON performance_schema.* TO 'converter_user'@'%';</code>. Esto permitir&iacute;a identificar cu&aacute;les consultas espec&iacute;ficas son las m&aacute;s lentas.
  </div>

  <div class="mejora">
    <strong>Configurar pool de conexiones en Django</strong>
    Con 30 threads activos actualmente el sistema est&aacute; bien, pero al crecer en usuarios se recomienda usar <code>CONN_MAX_AGE</code> en la configuraci&oacute;n de Django o una herramienta como ProxySQL para reusar conexiones y evitar que se saturen.
  </div>

  <div class="mejora">
    <strong>Mantener el buffer pool hit rate por encima del 95%</strong>
    Actualmente est&aacute; en 100%, lo cual es &oacute;ptimo. Si la base de datos crece en volumen, este porcentaje podr&iacute;a bajar. En ese caso se deber&iacute;a incrementar <code>innodb_buffer_pool_size</code> en la configuraci&oacute;n de MySQL para mantener m&aacute;s datos en memoria.
  </div>
</div>

</body>
</html>"""

with open('C:/Users/Isaac/Desktop/utez/converter-docs/docs/reporte-monitoreo.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML generado OK")
