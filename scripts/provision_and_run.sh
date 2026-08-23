#!/usr/bin/env bash
# Provision an Ubuntu VM, deploy the repo, run pytest tests, generate Allure report, and serve it.
# Usage: sudo ./scripts/provision_and_run.sh [--repo REPO_URL] [--branch BRANCH] [--dir REMOTE_DIR] [--port PORT]

set -euo pipefail

SCRIPT_NAME="provision_and_run.sh"

# Defaults (can be overridden via args or env)
REPO_URL="${REPO_URL:-}"
BRANCH="${BRANCH:-main}"
REMOTE_DIR="${REMOTE_DIR:-/home/rohith-azureuser/project}"
TEST_CMD="${TEST_CMD:-ENV=dev pytest playwright/tests/PracticeTestAutomationTests.py --alluredir=playwright/allure-results -v}"
PORT="${PORT:-8080}"

print_help(){
  cat <<EOF
Usage: sudo $SCRIPT_NAME [--repo REPO_URL] [--branch BRANCH] [--dir REMOTE_DIR] [--port PORT]

This script provisions an Ubuntu VM (installs packages), clones/pulls the repository,
creates a Python virtualenv, installs Python deps, runs tests using pytest, generates
an Allure report, and serves the report via a simple http server on port PORT.

ENV variables honored: REPO_URL, BRANCH, REMOTE_DIR, TEST_CMD, PORT

Example:
  sudo REPO_URL=git@github.com:youruser/robot-framework-project.git ./scripts/provision_and_run.sh
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO_URL="$2"; shift 2;;
    --branch) BRANCH="$2"; shift 2;;
    --dir) REMOTE_DIR="$2"; shift 2;;
    --port) PORT="$2"; shift 2;;
    --secrets-file) SECRETS_FILE="$2"; shift 2;;
    --help) print_help; exit 0;;
    *) echo "Unknown arg: $1"; print_help; exit 1;;
  esac
done

if [ -z "$REPO_URL" ]; then
  echo "REPO_URL is required. Pass with --repo or set REPO_URL env var." >&2
  print_help
  exit 1
fi

# optional secrets file path on the VM (passed via --secrets-file or env SECRETS_FILE)
SECRETS_FILE="${SECRETS_FILE:-}"

LOG=/var/log/provision_and_run.log
exec > >(tee -a "$LOG") 2>&1

echo "== Provision & Run starting: $(date)"
echo "Repo: $REPO_URL"
echo "Branch: $BRANCH"
echo "Remote dir: $REMOTE_DIR"

# 1) Install OS packages
echo "--> Installing apt packages"
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y git python3 python3-venv python3-pip wget unzip ca-certificates curl default-jre locales || true

# Ensure a non-root user exists (if running as sudo from a user)
if [ -n "${SUDO_USER:-}" ] && [ "$SUDO_USER" != "root" ]; then
  USERNAME="$SUDO_USER"
else
  USERNAME="rohith-azureuser"
fi

mkdir -p "$REMOTE_DIR"
chown -R "$USERNAME":"$USERNAME" "$(dirname "$REMOTE_DIR")" || true

# 2) Clone or update repository as the non-root user
echo "--> Fetching repository"
if [ -d "$REMOTE_DIR/.git" ]; then
  echo "Repository exists; fetching latest"
  su - "$USERNAME" -c "cd $REMOTE_DIR && git fetch --all && git checkout $BRANCH && git pull origin $BRANCH"
else
  echo "Cloning repository"
  su - "$USERNAME" -c "git clone --branch $BRANCH $REPO_URL $REMOTE_DIR"
fi

# 3) Create Python venv and install requirements
echo "--> Setting up Python virtualenv"
su - "$USERNAME" -c "python3 -m venv $REMOTE_DIR/venv"
su - "$USERNAME" -c "source $REMOTE_DIR/venv/bin/activate && pip install --upgrade pip setuptools wheel"

REQ_FILE="$REMOTE_DIR/requirements.txt"
if su - "$USERNAME" -c "[ -f $REQ_FILE ]"; then
  echo "Installing Python requirements from $REQ_FILE"
  su - "$USERNAME" -c "source $REMOTE_DIR/venv/bin/activate && pip install -r $REQ_FILE --use-deprecated=legacy-resolver"
else
  echo "No requirements.txt found; installing pytest and allure-pytest as fallback"
  su - "$USERNAME" -c "source $REMOTE_DIR/venv/bin/activate && pip install pytest allure-pytest"
fi

# 4) Install Playwright browsers & dependencies (if playwright used)
echo "--> Installing Playwright (if present) and browsers"
su - "$USERNAME" -c "source $REMOTE_DIR/venv/bin/activate && pip install playwright || true"
su - "$USERNAME" -c "source $REMOTE_DIR/venv/bin/activate && python -m playwright install || true"
su - "$USERNAME" -c "source $REMOTE_DIR/venv/bin/activate && python -m playwright install-deps || true"

# 5) Install Allure CLI (from GitHub releases) into /opt/allure if not present
if [ ! -x /usr/local/bin/allure ]; then
  echo "--> Installing Allure CLI"
  TMPDIR=$(mktemp -d)
  pushd "$TMPDIR"
  LATEST_URL=$(curl -s https://api.github.com/repos/allure-framework/allure2/releases/latest \
    | grep 'browser_download_url' \
    | grep 'allure-.*zip' \
    | head -n1 \
    | cut -d '"' -f 4)
  if [ -z "$LATEST_URL" ]; then
    echo "Could not determine Allure release URL; skipping Allure install" >&2
  else
    echo "Downloading Allure from $LATEST_URL"
    wget -q --show-progress -O allure.zip "$LATEST_URL"
    unzip -q allure.zip
    mkdir -p /opt
    mv allure-* /opt/allure || true
    ln -sf /opt/allure/bin/allure /usr/local/bin/allure
    echo "Installed Allure: $(/usr/local/bin/allure --version || echo 'unknown')"
  fi
  popd
  rm -rf "$TMPDIR"
fi

# 6) Run tests
echo "--> Running tests with: $TEST_CMD"
# If a secrets file was provided, copy it into the project and ensure it's only readable by the app user.
if [ -n "$SECRETS_FILE" ] && [ -f "$SECRETS_FILE" ]; then
  echo "--> Installing secrets from $SECRETS_FILE"
  cp "$SECRETS_FILE" "$REMOTE_DIR/.env"
  chown $USERNAME:$USERNAME "$REMOTE_DIR/.env" || true
  chmod 600 "$REMOTE_DIR/.env" || true
fi

# Run tests, sourcing the .env if present so env vars are available to pytest
su - "$USERNAME" -c "cd $REMOTE_DIR && source venv/bin/activate && set -o pipefail && if [ -f $REMOTE_DIR/.env ]; then set -a; source $REMOTE_DIR/.env; set +a; fi; $TEST_CMD"

# 7) Generate Allure report
ALLURE_INPUT="$REMOTE_DIR/playwright/allure-results"
ALLURE_OUTPUT="$REMOTE_DIR/playwright/allure-report"
if [ -d "$ALLURE_INPUT" ]; then
  echo "--> Generating Allure report from $ALLURE_INPUT to $ALLURE_OUTPUT"
  # Run generate and then open the report (background the open command so script can continue).
  su - "$USERNAME" -c "cd $REMOTE_DIR/playwright && source $REMOTE_DIR/venv/bin/activate && mkdir -p $ALLURE_OUTPUT && allure generate $ALLURE_INPUT --clean -o $ALLURE_OUTPUT && nohup allure open $ALLURE_OUTPUT > $REMOTE_DIR/allure-open.log 2>&1 &" || true
else
  echo "Allure results directory not found: $ALLURE_INPUT" >&2
fi

# 8) Serve report on $PORT
if [ -d "$ALLURE_OUTPUT" ]; then
  echo "--> Setting up systemd service to serve Allure report on port $PORT"
  SERVICE_PATH="/etc/systemd/system/allure-report.service"
  cat > "$SERVICE_PATH" <<SERVICE_EOF
[Unit]
Description=Allure Report Service
After=network.target

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$ALLURE_OUTPUT
ExecStart=/usr/bin/python3 -m http.server $PORT --directory $ALLURE_OUTPUT
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
SERVICE_EOF

  chmod 644 "$SERVICE_PATH"
  systemctl daemon-reload
  systemctl enable --now allure-report.service || true

  echo "Allure report service started. Port: $PORT"
  IP_ADDRS="$(hostname -I 2>/dev/null || echo '')"
  echo "VM local IPs: $IP_ADDRS"
  echo "If the VM has a public IP and port $PORT is open, open: http://<VM_PUBLIC_IP>:$PORT"
  echo "Recommended secure method: run an SSH tunnel from your laptop:"
  echo "  ssh -L $PORT:localhost:$PORT ${USERNAME}@<VM_HOST>"
  echo "  then open http://localhost:$PORT in your browser"
else
  echo "No Allure report generated; skipping service start." >&2
fi

echo "Provision & Run finished: $(date)"
echo "Logs: $LOG"

exit 0
