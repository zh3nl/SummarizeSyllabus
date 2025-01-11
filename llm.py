import requests

# Replace with your actual Claude API key
API_KEY = "your_claude_api_key_here"
API_URL = "https://api.anthropic.com/v1/complete"

def get_claude_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "model": "claude-3.5-sonnet",  # Specify the Claude model version
        "max_tokens_to_sample": 300,  # Limit the number of tokens in the response
        "temperature": 0.7  # Control randomness (0.0 = deterministic, 1.0 = more random)
    }

    response = requests.post(API_URL, json=data, headers=headers)

    if response.status_code == 200:
        return response.json().get("completion")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example usage
prompt = "Summarize this syllabus for me."
response = get_claude_response(prompt)
print(response)
