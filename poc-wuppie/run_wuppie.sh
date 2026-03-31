#!/bin/bash

BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}--- Wuppie TNO-Style Fuzzer Builder ---${NC}"

# 1. Bouw de Docker image
# We noemen de image 'wuppie-tno-fuzzer'
echo -e "${BLUE}[1/2] Container image bouwen...${NC}"
docker build -t wuppie-tno-fuzzer .

# Controleer of de build is gelukt
if [ $? -ne 0 ]; then
    echo -e "${RED} Fout tijdens het bouwen van de container. Controleer je Dockerfile.${NC}"
    exit 1
fi

# 2. Draai de container in het pentest-netwerk
echo -e "${BLUE}[2/2] Fuzzer starten in het netwerk...${NC}"

# Uitleg vlaggen:
# --rm          : Verwijder container na gebruik (houdt je systeem schoon)
# -v $(pwd):/app: Koppel de huidige map aan de container (zodat de JSON wordt opgeslagen)
# --network     : Gebruik het gezamenlijke netwerk van crAPI en Juice Shop
# -u $(id -u):$(id -g) : Zorg dat het JSON bestand jouw eigendom is (geen root-rechten nodig)

docker run --rm \
  -v "$(pwd):/app" \
  --network pentest-net \
  -u "$(id -u):$(id -g)" \
  wuppie-tno-fuzzer

# 3. Controleer of het resultaat er is
if [ -f "wuppie_results.json" ]; then
    echo -e "${GREEN}  Scan succesvol! Resultaten staan in: $(pwd)/wuppie_results.json${NC}"
else
    echo -e "${RED}  Scan klaar, maar wuppie_results.json is niet gevonden.${NC}"
fi