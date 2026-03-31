#!/bin/bash

echo "--- OWASP ZAP FULL ACTIVE SCAN Starten ---"
echo "Waarschuwing: Dit kan 15-30 minuten duren..."

# We gebruiken 'zap-full-scan.py' voor de actieve aanval
docker run --rm \
  -v $(pwd):/zap/wrk/:rw \
  --network pentest-net \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py \
  -t http://target-juiceshop:3000 \
  -r zap_full_report.html \
  -J zap_full_report.json