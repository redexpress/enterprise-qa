#!/bin/bash

set -e

PROJECT_ROOT=$(pwd)
DIST_DIR="$PROJECT_ROOT/dist"

# Get version from git tag, VERSION file, or fallback
GIT_TAG=$(git describe --tags --always --dirty 2>/dev/null)
BUILD_DATE=$(date +%Y%m%d)

if [ -n "$GIT_TAG" ]; then
    # Has git tag: use it directly (e.g., v1.0.0)
    FULL_VERSION="$GIT_TAG"
elif [ -f "$PROJECT_ROOT/VERSION" ]; then
    # No git tag, has VERSION file: use it with date suffix
    VERSION=$(cat "$PROJECT_ROOT/VERSION")
    FULL_VERSION="${VERSION}-${BUILD_DATE}"
else
    # No tag, no VERSION: use fallback with date suffix
    FULL_VERSION="v0.9.0-${BUILD_DATE}"
fi

PACKAGE_NAME="enterprise-qa-skill-${FULL_VERSION}"
TMP_DIR="$DIST_DIR/$PACKAGE_NAME"

echo "Version: $FULL_VERSION"

echo "Cleaning dist directory..."
rm -rf "$DIST_DIR"
mkdir -p "$TMP_DIR"

echo "Copying .claude..."
mkdir -p "${TMP_DIR}/.claude/commands"
mkdir -p "${TMP_DIR}/.claude/skills/enterprise-qa/tools"
cp "$PROJECT_ROOT/.claude/commands/enterprise-qa.md" "${TMP_DIR}/.claude/commands/"
cp "$PROJECT_ROOT/.claude/skills/enterprise-qa/SKILL.md" "${TMP_DIR}/.claude/skills/enterprise-qa/"
for f in "$PROJECT_ROOT/.claude/skills/enterprise-qa/tools"/*.py; do
    cp "$f" "${TMP_DIR}/.claude/skills/enterprise-qa/tools/"
done

echo "Copying knowledge..."
cp -R "$PROJECT_ROOT/knowledge" "$TMP_DIR/"

echo "Copying enterprise.db..."
cp "$PROJECT_ROOT/enterprise.db" "$TMP_DIR/"

echo "Copying config.yaml..."
cp "$PROJECT_ROOT/config.yaml.example" "$TMP_DIR/config.yaml"

echo "Copying requirements.txt..."
cp "$PROJECT_ROOT/requirements.txt" "$TMP_DIR/"


echo "Copying SKILL-README.md -> README.md..."
cp "$PROJECT_ROOT/SKILL-README.md" "$TMP_DIR/README.md"

echo "Creating archives..."

cd "$DIST_DIR"

# create zip (jar fallback)
if command -v zip &> /dev/null; then
    echo "Using zip..."
    zip -r "${PACKAGE_NAME}.zip" "$PACKAGE_NAME" > /dev/null
elif command -v jar &> /dev/null; then
    echo "Using jar (no-manifest)..."
    jar -cvfM "${PACKAGE_NAME}.zip" -C "$PACKAGE_NAME" . > /dev/null
else
    echo "Error: neither zip nor jar found"
    exit 1
fi

echo "Creating tar.gz..."
tar -czf "${PACKAGE_NAME}.tar.gz" "$PACKAGE_NAME"

cd "$PROJECT_ROOT"

echo "Done."
echo "Output:"
echo "  dist/${PACKAGE_NAME}.zip"
echo "  dist/${PACKAGE_NAME}.tar.gz"