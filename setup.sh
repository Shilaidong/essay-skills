#!/bin/bash
# Tavily Skill Setup - run this on a new machine after cloning

set -e

# Install Tavily CLI
if command -v pip3 &>/dev/null; then
    pip3 install tavily-cli
elif command -v pip &>/dev/null; then
    pip install tavily-cli
elif command -v brew &>/dev/null; then
    brew install tavily-cli
elif command -v uv &>/dev/null; then
    uv tool install tavily-cli
else
    curl -fsSL https://cli.tavily.com/install.sh | bash
fi

# Login with API key
tvly login --api-key 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

echo "Tavily CLI installed and authenticated. Skills ready to use."
