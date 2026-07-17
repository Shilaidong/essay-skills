import os, sys, argparse
import requests
from openai import OpenAI

API_KEY = os.environ.get("SENSENOVA_API_KEY", "")
BASE_URL = "https://token.sensenova.cn/v1"
MODEL = "sensenova-u1-fast"

def generate(prompt: str, size: str = "2752x1536", output: str = "infographic.png"):
    if not API_KEY:
        print("Error: Set SENSENOVA_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    resp = client.images.generate(model=MODEL, prompt=prompt, size=size, n=1)
    url = resp.data[0].url
    img = requests.get(url)
    with open(output, "wb") as f:
        f.write(img.content)
    print(f"Saved to {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate infographic via SenseNova U1 Fast")
    parser.add_argument("--prompt", required=True, help="Infographic description")
    parser.add_argument("--output", default="infographic.png", help="Output file path")
    parser.add_argument("--size", default="2752x1536", help="Image size (e.g. 2752x1536)")
    args = parser.parse_args()
    generate(args.prompt, args.size, args.output)
