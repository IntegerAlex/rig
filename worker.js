// SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
// SPDX-License-Identifier: GPL-3.0-only

/**
 * Cloudflare Worker to serve the rig installer script
 * Usage:
 *   curl https://rig-installer.gossorg.in | bash
 */

const REPO = "IntegerAlex/rig";
const BINARY_NAME = "rig";
const INSTALL_DIR = "$HOME/.local/bin";

const INSTALLER_SCRIPT = `#!/bin/bash
# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

set -e

BINARY_NAME="` + BINARY_NAME + `"
INSTALL_DIR="` + INSTALL_DIR + `"
RELEASE_URL="https://github.com/` + REPO + `/releases/latest"

echo "Installing rig - Opinionated system setup tool..."
echo "Repository: ` + REPO + `"
echo "Install directory: ` + INSTALL_DIR + `"

# Detect architecture
ARCH=$(uname -m)
case $ARCH in
    x86_64)
        ARCH="x86_64"
        ;;
    aarch64|arm64)
        ARCH="aarch64"
        ;;
    *)
        echo "❌ Unsupported architecture: $ARCH"
        echo "rig currently supports x86_64 and aarch64 architectures"
        exit 1
        ;;
esac

# Detect OS - only support Linux
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
if [ "$OS" != "linux" ]; then
    echo "❌ Unsupported operating system: $OS"
    echo "rig is designed for Linux systems only"
    exit 1
fi

echo "✅ Detected: Linux $ARCH"

# Check if running on Debian-based system (has apt)
if ! command -v apt-get &> /dev/null; then
    echo "❌ This installer requires a Debian-based Linux distribution (Ubuntu, Debian, etc.)"
    echo "apt-get command not found. Please install rig manually from:"
    echo "https://github.com/` + REPO + `/releases"
    exit 1
fi

echo "✅ Debian-based system detected"

# Get latest release tag
echo "📦 Fetching latest release..."
LATEST_TAG=$(curl -s "https://api.github.com/repos/` + REPO + `/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\\1/')

if [ -z "$LATEST_TAG" ]; then
    echo "❌ Error: Could not fetch latest release tag"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo "📋 Latest release: $LATEST_TAG"

# Construct download URL
ASSET_NAME="rig"
DOWNLOAD_URL="https://github.com/` + REPO + `/releases/download/$LATEST_TAG/$ASSET_NAME"

echo "⬇️  Downloading from: $DOWNLOAD_URL"

# Create install directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Download binary
TEMP_FILE=$(mktemp)
if curl -L -f -o "$TEMP_FILE" "$DOWNLOAD_URL"; then
    echo "✅ Download successful"
else
    echo "❌ Error: Failed to download binary"
    echo "Tried URL: $DOWNLOAD_URL"
    echo "Available releases: https://github.com/` + REPO + `/releases"
    rm -f "$TEMP_FILE"
    exit 1
fi

# Make binary executable
chmod +x "$TEMP_FILE"

# Install to target directory
INSTALL_PATH="$INSTALL_DIR/$BINARY_NAME"
mv "$TEMP_FILE" "$INSTALL_PATH"

echo "✅ Installed to: $INSTALL_PATH"

# Add to PATH for current session and run rig
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "⚠️  Adding $INSTALL_DIR to PATH for this session..."
    export PATH="$INSTALL_DIR:$PATH"

    echo ""
    echo "💡 For permanent PATH setup, add this to your ~/.bashrc or ~/.zshrc:"
    echo "   export PATH=\\$HOME/.local/bin:\\$PATH"
    echo "   Then run: source ~/.bashrc  (or source ~/.zshrc)"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "🚀 Running rig to show available tools..."
echo ""

# Run rig, but don't fail the installation if it fails
if "$INSTALL_PATH"; then
    echo ""
    echo "✅ rig completed successfully!"
else
    exit_code=$?
    echo ""
    echo "⚠️  rig exited with code $exit_code"
    echo "   This is normal if bootstrap failed (requires sudo) or you chose to exit."
    echo ""
    echo "📖 To run rig again:"
    echo "   rig              # Run rig (requires sudo for system tools)"
fi

echo ""
echo "📚 rig is an opinionated system setup tool for Linux"
echo "   It helps you install essential development tools with a beautiful UI"
`;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Handle CORS for preflight requests
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
      });
    }

    // Only allow GET requests
    if (request.method !== 'GET') {
      return new Response('Method not allowed', { status: 405 });
    }

    // Serve installer script
    if (url.pathname === '/' || url.pathname === '/install' || url.pathname === '/install.sh') {
      return new Response(INSTALLER_SCRIPT, {
        headers: {
          'Content-Type': 'text/plain; charset=utf-8',
          'Content-Disposition': 'inline; filename="install.sh"',
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'public, max-age=3600', // Cache for 1 hour
        },
      });
    }

    // Health check endpoint
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({
        status: 'ok',
        service: 'rig-installer',
        repo: REPO,
        binary: BINARY_NAME
      }), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });
    }

    // 404 for other paths
    return new Response('Not found', { status: 404 });
  },
};
