import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import system_prompt
from config import MAX_ITERS
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main():
    #print("Hello from sample-ai-agent!")

    model = 'gemini-2.0-flash-001'


    if len(sys.argv) == 1:
        print("Error: Prompt not provided", file=sys.stderr)
        sys.exit(1)

    verbose = "--verbose" in sys.argv

    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user",parts=[types.Part(text=user_prompt)]),
        ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )
    for _ in range(MAX_ITERS):
        try:
            response = client.models.generate_content(
                model=model,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                )
            )
            if verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            for candidate in response.candidates:
                messages.append(candidate.content)

            if response.function_calls:
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose=verbose)

                    if not function_call_result.parts[0].function_response.response:
                        raise Exception(f"Error: Function call returned no response")
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    messages.append(
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_function_response(
                                    name=function_call_part.name,
                                    response={"function_response": function_call_result.parts[0].function_response.response},
                                )
                            ],
                        )
                    )
            else:
                print(f"\nFinal response:\n {response.text}")
                break

        except Exception as e:
            raise Exception(f"Error: {str(e)}")




if __name__ == "__main__":
    main()