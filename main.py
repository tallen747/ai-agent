import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import call_function


def main():
    print("Hello from ai-agent!")

    load_dotenv()
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
    except RuntimeError as e:
        print(f"Error loading environment variables: {e}")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    prompt = args.user_prompt

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response  = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0 #He wasn't listening!!!
            )
    )

    if response.usage_metadata != None:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(response.text)
    else:
        raise RuntimeError("Response metadata is None. Unable to retrieve token counts.")

if __name__ == "__main__":
    main()
