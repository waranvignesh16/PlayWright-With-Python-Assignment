from openai import OpenAI
import os

# Create a client instance
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))  # replace with your key

# For GPT-3.5 (instruct style)
response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Say this is a test",
    max_tokens=7,
    temperature=0
)

print(response.choices[0].text)
