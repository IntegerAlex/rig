#!/bin/bash
# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
# Test script to validate the installer without actually installing

set -e

INSTALLER_URL="https://rig-installer.inquiry-akshatkotpalliwar.workers.dev"
TEMP_SCRIPT=$(mktemp)

echo "🧪 Testing rig installer..."
echo "📥 Downloading installer script..."

# Download the installer
if curl -s -o "$TEMP_SCRIPT" "$INSTALLER_URL"; then
    echo "✅ Download successful"
else
    echo "❌ Download failed"
    rm -f "$TEMP_SCRIPT"
    exit 1
fi

# Check if it's a bash script
if head -1 "$TEMP_SCRIPT" | grep -q "#!/bin/bash"; then
    echo "✅ Script has correct shebang"
else
    echo "❌ Script missing shebang"
    exit 1
fi

# Check if it contains rig-specific content
if grep -q "Installing rig - Opinionated system setup tool" "$TEMP_SCRIPT"; then
    echo "✅ Script contains rig branding"
else
    echo "❌ Script missing rig branding"
    exit 1
fi

if grep -q "IntegerAlex/rig" "$TEMP_SCRIPT"; then
    echo "✅ Script contains correct repository"
else
    echo "❌ Script missing correct repository"
    exit 1
fi

if grep -q "BINARY_NAME=\"rig\"" "$TEMP_SCRIPT"; then
    echo "✅ Script contains correct binary name"
else
    echo "❌ Script missing correct binary name"
    exit 1
fi

# Check for Debian-specific checks (Ubuntu/Debian/Linux Mint)
if grep -q "Debian-based system detected" "$TEMP_SCRIPT"; then
    echo "✅ Script includes Debian detection"
else
    echo "❌ Script missing Debian detection"
    exit 1
fi

# Check for apt or apt-get (support Linux Mint and derivatives)
if grep -qE 'command -v apt |command -v apt-get' "$TEMP_SCRIPT"; then
    echo "✅ Script checks for apt/apt-get"
else
    echo "❌ Script should check for apt or apt-get"
    exit 1
fi

echo ""
echo "🎉 All tests passed!"
echo "🚀 Installer is ready for use:"
echo "   curl $INSTALLER_URL | bash"
echo ""

# Clean up
rm -f "$TEMP_SCRIPT"
