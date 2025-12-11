import requests
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Cohere CHAT API with different models...")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Try different models
models_to_test = ["command-r-plus", "command-light", "command-nightly"]

for model in models_to_test:
    print(f"\nTesting model: {model}")
    url = "https://api.cohere.ai/v1/chat"
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "message": "Say hello",
        "max_tokens": 10
    }
    
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ SUCCESS! Response: {response.json().get('text', '')}")
        break
    else:
        print(f"❌ Failed: {response.json().get('message', 'Unknown error')}")