# SenseNova Skills Setup - Windows (PowerShell)

# 1. API Key & Config
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

# 2. Clone official repo & install all skills
$skillsDir = "$env:USERPROFILE\.config\opencode\skills"
$tmpDir = "$env:TEMP\sensenova-install"
if (Test-Path $tmpDir) { Remove-Item -Recurse -Force $tmpDir }
git clone https://github.com/OpenSenseNova/SenseNova-Skills.git --depth=1 $tmpDir
pip install httpx pillow python-dotenv openai -q
Get-ChildItem "$tmpDir\skills" -Directory | ForEach-Object {
  $target = Join-Path $skillsDir $_.Name
  if (Test-Path $target) { Remove-Item -Recurse -Force $target }
  Copy-Item -Recurse $_.FullName $target
}
Remove-Item -Recurse -Force $tmpDir

Write-Host "✅ SenseNova Skills installed!"
Write-Host "   All sn-* skills copied to: $skillsDir"
Write-Host "   API key and env vars configured."
