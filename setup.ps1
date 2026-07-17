# Skill Setup - run this on a new machine after cloning

# Tavily CLI
pip install tavily-cli
tvly login --api-key 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

# MiniMax CLI
& "$PSScriptRoot\minimax-cli\scripts\setup.ps1"

# SenseNova Skills (infographic generation)
& "$PSScriptRoot\sn-image-base\scripts\setup.ps1"
Write-Host "SenseNova skills ready: sn-image-base + sn-infographic"
