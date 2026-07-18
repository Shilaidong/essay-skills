#!/usr/bin/env bash
set -euo pipefail

SKILLS_DIR="${SKILLS_DIR:-}"
if [ -z "$SKILLS_DIR" ]; then
  if [ -d "$HOME/.config/opencode/skills" ]; then
    SKILLS_DIR="$HOME/.config/opencode/skills"
  elif [ -d "$HOME/.openclaw/skills" ]; then
    SKILLS_DIR="$HOME/.openclaw/skills"
  elif [ -d "$HOME/.hermes/skills" ]; then
    SKILLS_DIR="$HOME/.hermes/skills"
  else
    mkdir -p "$HOME/.config/opencode/skills"
    SKILLS_DIR="$HOME/.config/opencode/skills"
  fi
fi

REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

# API Key
export SN_API_KEY="sk-oR2i4htvsiA8bjPWhOPCR4ypsArXT8TE"
export SN_BASE_URL="https://token.sensenova.cn/v1"
export SN_CHAT_MODEL="sensenova-6.7-flash-lite"
export SN_CHAT_TYPE="openai-completions"
export SN_IMAGE_GEN_MODEL="sensenova-u1-fast"
export SN_IMAGE_GEN_MODEL_TYPE="sensenova"

for f in "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.profile"; do
  [ -f "$f" ] && grep -q "SN_API_KEY" "$f" 2>/dev/null || {
    cat >> "$f" << 'EOF'
export SN_API_KEY="sk-oR2i4htvsiA8bjPWhOPCR4ypsArXT8TE"
export SN_BASE_URL="https://token.sensenova.cn/v1"
export SN_CHAT_MODEL="sensenova-6.7-flash-lite"
export SN_CHAT_TYPE="openai-completions"
export SN_IMAGE_GEN_MODEL="sensenova-u1-fast"
export SN_IMAGE_GEN_MODEL_TYPE="sensenova"
EOF
  } && break
done

# Copy skills
for s in sn-image-base sn-infographic sn-image-imitate sn-image-resume \
         sn-deep-research sn-report-format-discovery sn-prepare-citations \
         sn-md-to-html-report; do
  [ -d "$REPO_DIR/$s" ] || continue
  rm -rf "$SKILLS_DIR/$s"
  cp -r "$REPO_DIR/$s" "$SKILLS_DIR/$s"
done

pip install httpx pillow python-dotenv openai -q
echo "SenseNova skills installed to: $SKILLS_DIR"
