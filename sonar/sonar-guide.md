# SonarQube — Guía de Análisis

**Proyectos:** `service-converter` (Django) + `converter-web-app` (React)  
**Dashboard:** http://localhost:9000  
**Credenciales:** `admin` / `Admin1234!xd`  
**Token:** `sqa_01e3d59042cdc95971b92409be48c00b8616eb5e`  
**Quality Gate:** UTEZ Gate (personalizado, sin requisito de coverage)

---

## Resultados del último análisis (2026-04-04)

### service-converter (Django)

| Métrica | Valor | Rating |
|---|---|---|
| Bugs | 0 | **A** |
| Vulnerabilidades | 0 | **A** |
| Security Hotspots | 1 (SAFE — Docker COPY) | — |
| Code Smells | 0 | **A** |
| Duplicación | 0.0% | **A** |

### converter-web-app (React)

| Métrica | Valor | Rating |
|---|---|---|
| Bugs | 0 | **A** |
| Vulnerabilidades | 0 | **A** |
| Security Hotspots | 0 | **A** |
| Code Smells | 0 | **A** |
| Duplicación | 0.0% | **A** |

> Quality Gate: **PASSED** en ambos proyectos.

---

## Cómo arrancar SonarQube

### Opción A — Docker Desktop
Abrir Docker Desktop → stack `utez` → play en `sonarqube_db` primero, luego `sonarqube`.

### Opción B — Terminal
```bash
docker start sonarqube_db sonarqube
```

Esperar ~20s y entrar a http://localhost:9000

> SonarQube corre sobre PostgreSQL. Los resultados persisten entre reinicios.

---

## Cómo correr el análisis

### Backend (service-converter)
```bash
cd C:/Users/Isaac/Desktop/utez/service-converter

sonar-scanner \
  -Dsonar.projectKey=service-converter \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=sqa_01e3d59042cdc95971b92409be48c00b8616eb5e
```

### Frontend (converter-web-app)
```bash
cd C:/Users/Isaac/Desktop/utez/converter-web-app

sonar-scanner \
  -Dsonar.projectKey=converter-web-app \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=sqa_01e3d59042cdc95971b92409be48c00b8616eb5e
```

### Ambos en paralelo
```bash
TOKEN="sqa_01e3d59042cdc95971b92409be48c00b8616eb5e"

(cd C:/Users/Isaac/Desktop/utez/service-converter && sonar-scanner -Dsonar.projectKey=service-converter -Dsonar.host.url=http://localhost:9000 -Dsonar.login=$TOKEN) &
(cd C:/Users/Isaac/Desktop/utez/converter-web-app && sonar-scanner -Dsonar.projectKey=converter-web-app -Dsonar.host.url=http://localhost:9000 -Dsonar.login=$TOKEN) &
wait
```

---

## Infraestructura

SonarQube corre con Docker Compose (`docker-compose.sonar.yml` en `C:/Users/Isaac/Desktop/utez/`):

- **SonarQube 26.3.0 Community** en puerto 9000
- **PostgreSQL 16** como base de datos (volumen `utez_sonarqube_pg_data`)

---

## Archivos de configuración

**`service-converter/sonar-project.properties`**
```properties
sonar.projectKey=service-converter
sonar.sources=.
sonar.exclusions=**/migrations/**,**/__pycache__/**,**/.git/**,**/logs/**,**/*.pyc
sonar.python.version=3
sonar.scm.disabled=true
```

**`converter-web-app/sonar-project.properties`**
```properties
sonar.projectKey=converter-web-app
sonar.sources=src
sonar.exclusions=**/node_modules/**,**/dist/**
sonar.scm.disabled=true
```
