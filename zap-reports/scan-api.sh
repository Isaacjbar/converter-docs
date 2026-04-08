#!/bin/bash
# ============================================================
# ZAP — Scan activo de la API (backend)
# Ejecutar desde Git Bash: bash scan-api.sh
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WIN_DIR="$(cygpath -w "$SCRIPT_DIR")"

echo ""
echo "============================================"
echo "  OWASP ZAP — API Scan"
echo "  api.converter.levsek.com.mx"
echo "============================================"
echo ""

# --- Obtener JWT token ---
echo "[1/3] Obteniendo JWT token..."

RESPONSE=$(curl -s -X POST https://api.converter.levsek.com.mx/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"zaptest@test.com","password":"ZapTest123!"}')

TOKEN=$(echo "$RESPONSE" | grep -o '"access":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "    Login fallido — registrando usuario de prueba..."
  curl -s -X POST https://api.converter.levsek.com.mx/auth/register/ \
    -H "Content-Type: application/json" \
    -d '{"email":"zaptest@test.com","username":"zaptest","password":"ZapTest123!"}' > /dev/null

  RESPONSE=$(curl -s -X POST https://api.converter.levsek.com.mx/auth/login/ \
    -H "Content-Type: application/json" \
    -d '{"email":"zaptest@test.com","password":"ZapTest123!"}')

  TOKEN=$(echo "$RESPONSE" | grep -o '"access":"[^"]*"' | cut -d'"' -f4)
fi

if [ -z "$TOKEN" ]; then
  echo "ERROR: No se pudo obtener el token JWT. Verifica que la API esté disponible."
  exit 1
fi

echo "    Token obtenido."

# --- Ejecutar ZAP ---
echo ""
echo "[2/3] Ejecutando scan (~15 min)..."
echo ""

MSYS_NO_PATHCONV=1 docker run --rm \
  -v "${WIN_DIR}:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py \
  -t /zap/wrk/openapi.yaml \
  -f openapi \
  -r api-report.html \
  -J api-report.json \
  -z "-config replacer.full_list(0).description=JWTAuth \
      -config replacer.full_list(0).enabled=true \
      -config replacer.full_list(0).matchtype=REQ_HEADER \
      -config replacer.full_list(0).matchstr=Authorization \
      -config replacer.full_list(0).replacement=Bearer ${TOKEN}"

# --- Abrir reporte ---
echo ""
echo "[3/3] Abriendo reporte..."
start "" "${SCRIPT_DIR}/api-report.html" 2>/dev/null
echo ""
echo "Reporte: ${SCRIPT_DIR}/api-report.html"
echo "============================================"
