#!/bin/bash
# SPDX-FileCopyrightText: Copyright (C) 2025 Akshat Kotpalliwar (alias IntegerAlex) <inquiry.akshatkotpalliwar@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only
# Release script for creating and publishing rig binary releases

set -e

# Get version from package.json
VERSION=$(grep -E '"version":' package.json | sed -E 's/.*"version": "([^"]+)".*/\1/')

if [ -z "$VERSION" ]; then
  echo "❌ Could not determine version from package.json"
  exit 1
fi

TAG="v${VERSION}"
BINARY="dist/rig"

echo "🔨 Building binary for release ${TAG}..."

# Build the binary
if ! npm run build; then
  echo "❌ Build failed!"
  exit 1
fi

# Check if binary exists
if [ ! -f "$BINARY" ]; then
  echo "❌ Binary not found at $BINARY"
  exit 1
fi

echo "✅ Binary built successfully!"
echo "📊 Binary size: $(du -h $BINARY | cut -f1)"
file $BINARY

# Check if tag already exists
if git rev-parse "$TAG" >/dev/null 2>&1; then
  echo "⚠️  Tag $TAG already exists. Do you want to delete and recreate it? (y/N)"
  read -r response
  if [[ "$response" =~ ^[Yy]$ ]]; then
    git tag -d "$TAG"
    git push origin ":refs/tags/$TAG" 2>/dev/null || true
  else
    echo "❌ Aborted. Tag $TAG already exists."
    exit 1
  fi
fi

# Create and push tag
echo "🏷️  Creating tag $TAG..."
git tag -a "$TAG" -m "Release $TAG"
git push origin "$TAG"

# Check if release already exists
if gh release view "$TAG" >/dev/null 2>&1; then
  echo "⚠️  Release $TAG already exists. Do you want to delete and recreate it? (y/N)"
  read -r response
  if [[ "$response" =~ ^[Yy]$ ]]; then
    gh release delete "$TAG" --yes
  else
    echo "❌ Aborted. Release $TAG already exists."
    exit 1
  fi
fi

# Create release with binary
echo "🚀 Creating GitHub release $TAG..."
gh release create "$TAG" "$BINARY" \
  --title "$TAG" \
  --notes "Release $TAG - Binary distribution of rig system setup tool

## Installation

Download the binary and make it executable:

\`\`\`bash
chmod +x rig
./rig
\`\`\`

## What's included

- Standalone native binary (no runtime dependencies)
- All dependencies bundled
- Native x86_64 Linux executable (Ubuntu 20+, Debian 11+, etc.)"

echo "✅ Release created successfully!"
echo "🔗 Release URL: https://github.com/IntegerAlex/rig/releases/tag/$TAG"
