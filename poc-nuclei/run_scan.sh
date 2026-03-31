#!/bin/bash

echo "--- Nuclei Scanner Starten ---"

# We draaien Nuclei via Docker
# -v $(pwd):/app  -> Slaat de resultaten op in de huidige map
# --network pentest-net -> Zorgt dat Nuclei de Juice Shop kan 'zien'
docker run --rm \
  -v $(pwd):/app \
  --network pentest-net \
  projectdiscovery/nuclei:latest \
  -target http://target-juiceshop:3000 \
  -rate-limit 10 \
  -tags cve,exposure,vulnerability \
  -o /app/nuclei_results.txt