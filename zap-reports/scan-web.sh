#!/bin/bash
# ============================================================
# ZAP — Scan pasivo del frontend (web)
# Ejecutar desde Git Bash: bash scan-web.sh
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WIN_DIR="$(cygpath -w "$SCRIPT_DIR")"

echo ""
echo "============================================"
echo "  OWASP ZAP — Web Baseline Scan"
echo "  converter.levsek.com.mx"
echo "============================================"
echo ""

# --- Ejecutar ZAP ---
echo "[1/2] Ejecutando scan (~5 min)..."
echo ""

MSYS_NO_PATHCONV=1 docker run --rm \
  -v "${WIN_DIR}:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
  -t https://converter.levsek.com.mx \
  -r web-report.html \
  -J web-report.json \
  -c /zap/wrk/baseline-config.tsv

# --- Abrir reporte ---
echo ""
echo "[2/2] Abriendo reporte..."
start "" "${SCRIPT_DIR}/web-report.html" 2>/dev/null
echo ""
echo "Reporte: ${SCRIPT_DIR}/web-report.html"
echo "============================================"
