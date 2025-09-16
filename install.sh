#!/usr/bin/env bash
set -euo pipefail

echo "[AI-Logs] This installer will set up AI-Logs on Debian 11: install Docker, write config, compose up."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_DIR="$SCRIPT_DIR/deploy"
ENV_FILE="$DEPLOY_DIR/.env"

read -r -p "Browser address (IP/domain) [$(hostname -I 2>/dev/null | awk '{print $1}')]:" BROWSER_ADDR
BROWSER_ADDR=${BROWSER_ADDR:-$(hostname -I 2>/dev/null | awk '{print $1}')}

read -r -p "Admin username [admin]: " ADMIN_USER; ADMIN_USER=${ADMIN_USER:-admin}
read -r -s -p "Admin password [admin123]: " ADMIN_PASS; echo; ADMIN_PASS=${ADMIN_PASS:-admin123}
read -r -p "Admin email [admin@example.com]: " ADMIN_EMAIL; ADMIN_EMAIL=${ADMIN_EMAIL:-admin@example.com}

read -r -p "Use built-in MinIO? (Y/n): " USE_MINIO
USE_MINIO=${USE_MINIO:-Y}

S3_ENDPOINT=""; S3_ACCESS_KEY=""; S3_SECRET_KEY=""; S3_BUCKET="ailogs"; S3_REGION="us-east-1"
if [[ "${USE_MINIO}" =~ ^[Nn]$ ]]; then
  read -r -p "S3 endpoint URL: " S3_ENDPOINT
  read -r -p "S3 access key: " S3_ACCESS_KEY
  read -r -p "S3 secret key: " S3_SECRET_KEY
  read -r -p "S3 bucket [ailogs]: " _B; S3_BUCKET=${_B:-ailogs}
  read -r -p "S3 region [us-east-1]: " _R; S3_REGION=${_R:-us-east-1}
fi

read -r -p "Configure SSO (OIDC)? (y/N): " USE_OIDC
USE_OIDC=${USE_OIDC:-N}
OIDC_CLIENT_ID=""; OIDC_CLIENT_SECRET=""; OIDC_DISCOVERY_URL=""
if [[ "${USE_OIDC}" =~ ^[Yy]$ ]]; then
  read -r -p "OIDC Client ID: " OIDC_CLIENT_ID
  read -r -p "OIDC Client Secret: " OIDC_CLIENT_SECRET
  read -r -p "OIDC Discovery URL: " OIDC_DISCOVERY_URL
fi

read -r -p "Enable OpenSearch full-text search? (y/N): " USE_OS
USE_OS=${USE_OS:-N}

echo "[AI-Logs] Installing Docker & Compose..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y ca-certificates curl gnupg lsb-release git python3
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "[AI-Logs] Writing config to deploy/.env ..."
mkdir -p "$DEPLOY_DIR"

DB_URL="postgresql+psycopg://ailog:ailog@db:5432/ailog"
API_URL="http://${BROWSER_ADDR}:8000"
FRONTEND_URL="http://${BROWSER_ADDR}:8080"

# Fernet & JWT
KEY1=$(openssl rand -base64 32 | tr '+/' '-_' | tr -d '\n')
KEY2=$(openssl rand -base64 32 | tr '+/' '-_' | tr -d '\n')
JWT=$(openssl rand -base64 48 | tr -d '\n')

cat > "$ENV_FILE" <<EOF
DATABASE_URL=${DB_URL}
FERNET_KEYS=${KEY1};${KEY2}
JWT_SECRET=${JWT}
ADMIN_USER=${ADMIN_USER}
ADMIN_PASS=${ADMIN_PASS}
ADMIN_EMAIL=${ADMIN_EMAIL}
CORS_ORIGINS=${FRONTEND_URL}
REDIS_URL=redis://redis:6379/0

S3_ENDPOINT=${S3_ENDPOINT}
S3_ACCESS_KEY=${S3_ACCESS_KEY}
S3_SECRET_KEY=${S3_SECRET_KEY}
S3_BUCKET=${S3_BUCKET}
S3_REGION=${S3_REGION}

OIDC_CLIENT_ID=${OIDC_CLIENT_ID}
OIDC_CLIENT_SECRET=${OIDC_CLIENT_SECRET}
OIDC_DISCOVERY_URL=${OIDC_DISCOVERY_URL}
OIDC_REDIRECT_URI=${API_URL}/auth/oidc/callback

FRONTEND_URL=${FRONTEND_URL}
API_URL=${API_URL}
RATE_LIMIT_DEFAULT=60/minute
EOF

pushd "$DEPLOY_DIR" >/dev/null

# Remove legacy 'version:' key if present
sed -i '/^version:/d' docker-compose.yml || true
sed -i '/^version:/d' docker-compose.opensearch.yml || true

echo "[AI-Logs] Building and starting containers..."
if [[ "${USE_OS}" =~ ^[Yy]$ ]]; then
  docker compose --env-file .env -f docker-compose.yml -f docker-compose.opensearch.yml up -d --build
else
  docker compose --env-file .env -f docker-compose.yml up -d --build
fi

echo "[AI-Logs] Done."
echo "Frontend:  ${FRONTEND_URL}"
echo "API ready: ${API_URL}/ready"

popd >/dev/null
