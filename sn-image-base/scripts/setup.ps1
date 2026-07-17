pip install httpx pillow python-dotenv openai
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
Write-Host "sn-image-base installed. Python deps + env vars configured."
