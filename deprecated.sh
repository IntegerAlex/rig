#!/usr/bin/env bash
set -Eeuo pipefail

LOG_FILE="/var/log/setup.log"

# -----------------------------
# Logging setup
# -----------------------------
sudo touch "$LOG_FILE"
sudo chmod 644 "$LOG_FILE"

log() {
  echo "[$(date '+%F %T')] $*" >>"$LOG_FILE"
}

print() { echo -e "$*" >&2; }

info()  { print "\033[0;34mℹ $1\033[0m"; log "[INFO] $1"; }
ok()    { print "\033[0;32m✔ $1\033[0m"; log "[OK] $1"; }
warn()  { print "\033[1;33m⚠ $1\033[0m"; log "[WARN] $1"; }
err()   { print "\033[0;31m✖ $1\033[0m"; log "[ERROR] $1"; }

# -----------------------------
# Error handling
# -----------------------------
on_error() {
  local code=$?
  err "Script failed on line $1 (exit code $code)"
  err "Check log: $LOG_FILE"
  exit "$code"
}

trap 'on_error $LINENO' ERR

# -----------------------------
# Run helper
# -----------------------------
run() {
  log "CMD: $*"
  "$@" >>"$LOG_FILE" 2>&1
}

# -----------------------------
# Ask helper
# -----------------------------
ask() {
  read -rp "$(echo -e "\033[0;34m👉 Install $1? [y/N]: \033[0m")" reply
  [[ "$reply" =~ ^[Yy]$ ]]
}

# -----------------------------
# Bootstrap
# -----------------------------
info "Initializing system"
run sudo apt update
run sudo apt install -y ca-certificates curl wget gnupg lsb-release

# -----------------------------
# GitHub CLI
# -----------------------------
if ask "GitHub CLI (gh)"; then
  info "Installing GitHub CLI"

  run sudo mkdir -p /etc/apt/keyrings
  run bash -c 'wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg >/dev/null'

  run sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg

  run bash -c 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
    | sudo tee /etc/apt/sources.list.d/github-cli.list >/dev/null'

  run sudo apt update
  run sudo apt install -y gh

  ok "GitHub CLI installed"
fi

# -----------------------------
# uv
# -----------------------------
if ask "uv (Astral Python manager)"; then
  run bash -c "curl -LsSf https://astral.sh/uv/install.sh | sh"
  ok "uv installed"
fi

# -----------------------------
# Node.js via nvm
# -----------------------------
if ask "Node.js (via nvm)"; then
  run bash -c "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash"

  export NVM_DIR="$HOME/.nvm"
  # shellcheck disable=SC1090
  [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

  run nvm install 24
  run nvm use 24

  ok "Node.js installed"
fi

# -----------------------------
# pnpm
# -----------------------------
if ask "pnpm"; then
  run corepack enable pnpm
  ok "pnpm enabled"
fi

# -----------------------------
# Neovim (latest)
# -----------------------------
if ask "Neovim (latest release)"; then
  TMP="$(mktemp)"
  run curl -L https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.tar.gz -o "$TMP"

  run sudo rm -rf /opt/nvim-linux-x86_64
  run sudo tar -C /opt -xzf "$TMP"
  run sudo ln -sf /opt/nvim-linux-x86_64/bin/nvim /usr/local/bin/nvim

  ok "Neovim installed"
fi

# -----------------------------
# btop
# -----------------------------
if ask "btop"; then
  run sudo apt install -y btop
  ok "btop installed"
fi

# -----------------------------
# nginx
# -----------------------------
if ask "nginx"; then
  run sudo apt install -y nginx
  run sudo systemctl enable nginx
  ok "nginx installed"
fi

# -----------------------------
# Certbot
# -----------------------------
if ask "Certbot (Let's Encrypt)"; then
  run sudo apt install -y python3 python3-dev python3-venv libaugeas-dev gcc

  run sudo mkdir -p /opt/certbot

  if [ ! -x /opt/certbot/bin/python ]; then
    run sudo python3 -m venv /opt/certbot
  fi

  run sudo /opt/certbot/bin/pip install --upgrade pip
  run sudo /opt/certbot/bin/pip install certbot certbot-nginx
  run sudo ln -sf /opt/certbot/bin/certbot /usr/bin/certbot

  ok "Certbot installed"
fi

# -----------------------------
# Firewall (not enabled)
# -----------------------------
if ask "Install firewall (UFW)"; then
  run sudo apt install -y ufw
  run sudo ufw default deny incoming
  run sudo ufw default allow outgoing
  run sudo ufw allow 22/tcp
  run sudo ufw allow 80
  run sudo ufw allow 443

  warn "UFW configured but NOT enabled"
fi

# -----------------------------
# Fail2ban (not started)
# -----------------------------
if ask "Install Fail2ban"; then
  run sudo apt install -y fail2ban

  run sudo tee /etc/fail2ban/jail.local >/dev/null <<'EOF'
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 5
backend = systemd

[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
EOF

  warn "Fail2ban installed but NOT started"
fi

# -----------------------------
# Image Viewer
# -----------------------------
if ask "Advance Image Viewer"; then
  run bash -c "curl -fsSL https://advance-image-viewer.gossorg.in | bash"
  ok "Image viewer installed"
fi

# -----------------------------
# Curlpad
# -----------------------------
if ask "curlpad"; then
  run bash -c "curl -fsSL curlpad-installer.gossorg.in/install.sh | bash"
  ok "curlpad installed"
fi

# -----------------------------
# Dev tools
# -----------------------------
if ask "Developer tools"; then
  run sudo apt install -y \
    openssl \
    clangd \
    build-essential \
    pkg-config \
    cmake \
    git
  ok "Developer tools installed"
fi

echo
ok "Setup completed successfully 🎉"
print "📄 Log file: $LOG_FILE"
print "🔁 Restart shell: source ~/.bashrc"

