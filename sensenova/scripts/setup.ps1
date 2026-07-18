# SenseNova Skills Setup
param([string]$SkillsDir = "")

if (-not $SkillsDir) {
  if (Test-Path "$env:USERPROFILE\.config\opencode\skills") {
    $SkillsDir = "$env:USERPROFILE\.config\opencode\skills"
  } elseif (Test-Path "$env:USERPROFILE\.openclaw\skills") {
    $SkillsDir = "$env:USERPROFILE\.openclaw\skills"
  } elseif (Test-Path "$env:USERPROFILE\.hermes\skills") {
    $SkillsDir = "$env:USERPROFILE\.hermes\skills"
  } else {
    $SkillsDir = "$env:USERPROFILE\.config\opencode\skills"
    New-Item -ItemType Directory -Path $SkillsDir -Force | Out-Null
  }
}

$RepoDir = Split-Path -Parent $PSScriptRoot
$RepoDir = Split-Path -Parent $RepoDir

# API Key
$envVars = @{
  SN_API_KEY = "sk-oR2i4htvsiA8bjPWhOPCR4ypsArXT8TE"
  SN_BASE_URL = "https://token.sensenova.cn/v1"
  SN_CHAT_MODEL = "sensenova-6.7-flash-lite"
  SN_CHAT_TYPE = "openai-completions"
  SN_IMAGE_GEN_MODEL = "sensenova-u1-fast"
  SN_IMAGE_GEN_MODEL_TYPE = "sensenova"
}
foreach ($key in $envVars.Keys) {
  [Environment]::SetEnvironmentVariable($key, $envVars[$key], "User")
}

# Copy skills
$skills = @('sn-image-base','sn-infographic','sn-image-imitate','sn-image-resume',
            'sn-deep-research','sn-report-format-discovery','sn-prepare-citations',
            'sn-md-to-html-report')
foreach ($s in $skills) {
  $src = Join-Path $RepoDir $s
  $dst = Join-Path $SkillsDir $s
  if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
  if (Test-Path $src) { Copy-Item -Recurse $src $dst }
}

# Python deps
pip install httpx pillow python-dotenv openai -q

Write-Host "SenseNova skills installed to: $SkillsDir"
