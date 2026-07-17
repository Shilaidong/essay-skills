#!/usr/bin/env bash
set -euo pipefail
npm install -g mmx-cli
mkdir -p ~/.mmx
cat > ~/.mmx/config.json << 'EOF'
{
  "region": "cn",
  "api_key": "sk-cp-JoIfnsjVVh9cj3XTsh1qJp5h7-ycQ123inQ_iCH6pZQQk0XETc-EVhmnigVWvKC5ZMs93tDfvdotIs3XeQ6QjBx3D2pbLuRVHGZngtiEYItYxCJskSE-k2U"
}
EOF
echo "MiniMax CLI installed and configured."
