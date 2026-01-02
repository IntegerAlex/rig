#!/bin/bash
# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
# Build script for creating rig binary using PyInstaller

set -e

echo "🔨 Building rig binary with PyInstaller..."

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller is not installed. Installing..."
    pip install pyinstaller
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ __pycache__/ *.spec.bak

# Build the binary
echo "📦 Building binary..."
pyinstaller rig.spec

# Check if build was successful
if [ -f "dist/rig" ]; then
    echo "✅ Build successful! Binary created at: dist/rig"
    echo "📊 Binary size: $(du -h dist/rig | cut -f1)"
    echo ""
    echo "To test the binary, run: ./dist/rig"
else
    echo "❌ Build failed! Check the output above for errors."
    exit 1
fi


