#!/usr/bin/env bash
set -euo pipefail

# create-github-release.sh
# Create a GitHub release with all template zip files
# Usage: create-github-release.sh <version>

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"

# Remove 'v' prefix from version for release title
VERSION_NO_V=${VERSION#v}

gh release create "$VERSION" \
  .genreleases/spec-ops-template-copilot-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-copilot-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-claude-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-claude-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-gemini-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-gemini-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-cursor-agent-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-cursor-agent-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-opencode-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-opencode-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-qwen-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-qwen-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-windsurf-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-windsurf-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-codex-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-codex-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-kilocode-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-kilocode-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-auggie-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-auggie-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-roo-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-roo-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-codebuddy-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-codebuddy-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-qoder-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-qoder-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-amp-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-amp-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-shai-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-shai-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-q-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-q-ps-"$VERSION".zip \
  .genreleases/spec-ops-template-bob-sh-"$VERSION".zip \
  .genreleases/spec-ops-template-bob-ps-"$VERSION".zip \
  --title "Spec Ops Templates - $VERSION_NO_V" \
  --notes-file release_notes.md