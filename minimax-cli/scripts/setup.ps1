npm install -g mmx-cli
$configDir = "$env:USERPROFILE\.mmx"
New-Item -ItemType Directory -Path $configDir -Force | Out-Null
@"
{
  "region": "cn",
  "api_key": "sk-cp-JoIfnsjVVh9cj3XTsh1qJp5h7-ycQ123inQ_iCH6pZQQk0XETc-EVhmnigVWvKC5ZMs93tDfvdotIs3XeQ6QjBx3D2pbLuRVHGZngtiEYItYxCJskSE-k2U"
}
"@ | Set-Content -Path "$configDir\config.json" -Encoding UTF8
Write-Host "MiniMax CLI installed and configured."
