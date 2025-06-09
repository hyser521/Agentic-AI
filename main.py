import os
from dotenv import load_dotenv
from google import genai
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) <= 1:
    print("no prompt added.")
    exit(1)

prompt = sys.argv[1]
messages = [genai.types.Content(role="user", parts=[genai.types.Part(text=prompt)])]
content_response = client.models.generate_content(model = "gemini-2.0-flash-001", contents = messages)
if len(sys.argv) == 3:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {content_response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {content_response.usage_metadata.candidates_token_count}")
print(content_response.text)
exit(0)