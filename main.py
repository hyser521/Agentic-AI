import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function
from prompts import system_prompt
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    
    if not args:
        print("no prompt added.")
        exit(1)

    prompt = " ".join(args)
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    if verbose:
        print(f"User prompt: {prompt}")

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    for x in range (0, 20):
        model_name = "gemini-2.0-flash-001"

        content_response = client.models.generate_content(
            model = model_name, 
            contents = messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]))
        
        if verbose:
            print(f"Prompt tokens: {content_response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {content_response.usage_metadata.candidates_token_count}")
            print(content_response.text)

        for candidate in content_response.candidates:
            messages.append(candidate.content)
        
        if content_response.function_calls:
            for function_call_part in content_response.function_calls:
                function_call_result = call_function(function_call_part, verbose)
                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                ):
                    raise Exception("empty function call result")
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(function_call_result)
        else:
            print(content_response.text)
            return

if __name__ == "__main__":
    main()