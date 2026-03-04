import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import sys


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

    model="gemini-2.5-flash"
    contents=messages
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
        temperature=0 #He/She wasn't listening!!!
        )

    # response = gen_content(client, model, contents, config, args)

    for i in range(20):
        contents = gen_content(client, model, contents, config, args)
        if contents is None:
            break
        if contents is not None and i == 19:
            sys.exit("Reached maximum number of iterations (20) without receiving a final response. Exiting to prevent infinite loop.")
    

def gen_content(client, model, contents, config, args):
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config
    )

    messages = contents
    for candidate in response.candidates:
        if candidate != None:
            messages.append(candidate.content)

    if response.usage_metadata != None:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        # print(response.text)
        if response.function_calls != None and len(response.function_calls) > 0:
            function_responses = []
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name} ({function_call.args})")
                function_call_response = call_function(function_call, verbose=args.verbose)
                if len(function_call_response.parts) == 0:
                    raise Exception("Function call response has no parts. Unable to retrieve function response content.")
                if not function_call_response.parts[0].function_response:
                    raise Exception("Function call response part has no function response. Unable to retrieve function response content.")
                if not function_call_response.parts[0].function_response.response:
                    raise Exception("Function call response part function response has no 'response' field. Unable to retrieve function response content.")
                function_responses.append(function_call_response.parts[0])
                if args.verbose:
                    print(f"-> {function_call_response.parts[0].function_response.response}")
            messages.append(types.Content(role="user",parts=function_responses))
            return messages
        else:
            print(response.text)
            return None
                
    else:
        raise RuntimeError("Response metadata is None. Unable to retrieve token counts.")

if __name__ == "__main__":
    main()
