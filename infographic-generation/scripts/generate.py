import sys, argparse
import requests
from openai import OpenAI

API_KEY = "sk-oR2i4htvsiA8bjPWhOPCR4ypsArXT8TE"
BASE_URL = "https://token.sensenova.cn/v1"
MODEL = "sensenova-u1-fast"

def generate(prompt: str, size: str = "2752x1536", output: str = "infographic.png"):
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    resp = client.images.generate(model=MODEL, prompt=prompt, size=size, n=1)
    url = resp.data[0].url
    img = requests.get(url)
    with open(output, "wb") as f:
        f.write(img.content)
    print(f"Saved to {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate infographic via SenseNova U1 Fast")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", default="infographic.png")
    parser.add_argument("--size", default="2752x1536")
    args = parser.parse_args()
    generate(args.prompt, args.size, args.output)
