1. Het netwerk aanmaken

Zorg dat het centrale netwerk bestaat voordat je de containers start:
Bash

docker network create pentest-net

2. Targets opstarten

Navigeer naar de hoofdmap van het project en start de Docker Compose stacks.
OWASP Juice Shop
Bash

cd targets/juiceshop
docker compose up -d

Beschikbaar op: http://localhost:3000
OWASP crAPI
Bash

cd ../crapi
docker compose up -d

Beschikbaar op: http://localhost:8888 (Dashboard) en http://localhost:8025 (Mailhog)
