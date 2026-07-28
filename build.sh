#!/bin/bash
# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
# Build script for creating rig binary using scriptc

set -e

echo "🔨 Building rig binary with scriptc..."

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
  echo "📦 Installing dependencies..."
  npm install
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ .scriptc/

# Build the binary
echo "📦 Building binary..."
./node_modules/.bin/scriptc build src/main.ts -o dist/rig --no-keep-c --dynamic

# Check if build was successful
if [ -f "dist/rig" ]; then
  echo "✅ Build successful! Binary created at: dist/rig"
  echo "📊 Binary size: $(du -h dist/rig | cut -f1)"
  echo ""
  echo "To test the binary, run: ./dist/rig"
  file dist/rig
else
  echo "❌ Build failed! Check the output above for errors."
  exit 1
fi
