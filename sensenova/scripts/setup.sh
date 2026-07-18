#!/usr/bin/env bash
set -euo pipefail

# 1. API Key & Config
export SN_API_KEY="sk-oR2i4htvsiA8bjPWhOPCR4ypsArXT8TE"
export SN_BASE_URL="https://token.sensenova.cn/v1"
export SN_CHAT_MODEL="sensenova-6.7-flash-lite"
export SN_CHAT_TYPE="openai-completions"
export SN_IMAGE_GEN_MODEL="sensenova-u1-fast"
export SN_IMAGE_GEN_MODEL_TYPE="sensenova"

# Persist to shell profile
PROFILE=""
for f in "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.profile"; do
  [ -f "$f" ] && PROFILE="$f" && break
done
[ -z "$PROFILE" ] && PROFILE="$HOME/.profile"

cat >> "$PROFILE" << 'EOF'

# SenseNova Skills
export SN_API_KEY="sk-oR2i4htvsiA8bjPWhOPCR4ypsArXT8TE"
export SN_BASE_URL="https://token.sensenova.cn/v1"
export SN_CHAT_MODEL="sensenova-6.7-flash-lite"
export SN_CHAT_TYPE="openai-completions"
export SN_IMAGE_GEN_MODEL="sensenova-u1-fast"
export SN_IMAGE_GEN_MODEL_TYPE="sensenova"
EOF

# 2. Detect skills directory
SKILLS_DIR=""
if [ -n "${OPENCLAW_SHELL:-}" ] && [ -d "$HOME/.openclaw/skills" ]; then
  SKILLS_DIR="$HOME/.openclaw/skills"
elif [ -d "$HOME/.hermes/skills" ]; then
  SKILLS_DIR="$HOME/.hermes/skills"
elif [ -d "$HOME/.config/opencode/skills" ]; then
  SKILLS_DIR="$HOME/.config/opencode/skills"
elif [ -d "$HOME/.openclaw/skills" ]; then
  SKILLS_DIR="$HOME/.openclaw/skills"
else
  mkdir -p "$HOME/.config/opencode/skills"
  SKILLS_DIR="$HOME/.config/opencode/skills"
fi

# 3. Clone official repo & install all skills
TMPDIR=$(mktemp -d)
git clone https://github.com/OpenSenseNova/SenseNova-Skills.git --depth=1 "$TMPDIR"
pip install httpx pillow python-dotenv openai -q

for d in "$TMPDIR/skills/"*/; do
  name=$(basename "$d")
  target="$SKILLS_DIR/$name"
  rm -rf "$target"
  cp -r "$d" "$target"
done
rm -rf "$TMPDIR"

echo "✅ SenseNova Skills installed!"
echo "   All sn-* skills copied to: $SKILLS_DIR"
echo "   API key and env vars configured."
