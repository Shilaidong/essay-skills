#!/usr/bin/env bash
set -euo pipefail
pip install httpx pillow python-dotenv openai

# Write env vars to profile so they persist
PROFILE_FILE=""
if [ -f "$HOME/.zshrc" ]; then
  PROFILE_FILE="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
  PROFILE_FILE="$HOME/.bashrc"
elif [ -f "$HOME/.bash_profile" ]; then
  PROFILE_FILE="$HOME/.bash_profile"
else
  PROFILE_FILE="$HOME/.profile"
fi

cat >> "$PROFILE_FILE" << 'EOF'

# SenseNova-Skills env vars
export SN_API_KEY="sk-oR2i4htvsiA8bjPWhOPCR4ypsArXT8TE"
export SN_BASE_URL="https://token.sensenova.cn/v1"
export SN_CHAT_MODEL="sensenova-6.7-flash-lite"
export SN_CHAT_TYPE="openai-completions"
export SN_IMAGE_GEN_MODEL="sensenova-u1-fast"
export SN_IMAGE_GEN_MODEL_TYPE="sensenova"
EOF

# Also export for current session
export SN_API_KEY="sk-oR2i4htvsiA8bjPWhOPCR4ypsArXT8TE"
export SN_BASE_URL="https://token.sensenova.cn/v1"
export SN_CHAT_MODEL="sensenova-6.7-flash-lite"
export SN_CHAT_TYPE="openai-completions"
export SN_IMAGE_GEN_MODEL="sensenova-u1-fast"
export SN_IMAGE_GEN_MODEL_TYPE="sensenova"

echo "sn-image-base installed. Python deps + env vars configured."
