import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
import functions.get_files_info as gf
import prompts
import call_function as cf

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("api_key None")

client = genai.Client(api_key = api_key)
model_name = "gemini-2.5-flash"

my_config=types.GenerateContentConfig(tools=[cf.available_functions], 
    system_instruction=prompts.system_prompt,
    temperature=0)


def main():
    ai_start()

def ai_start():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    for _ in range(20):
        if generate(args, messages):
            return
    print("Max iterations reached...")


def generate(args, messages):
    # Now we can access `args.user_prompt`
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=my_config
    )
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    if args.verbose: print(f"User prompt: {args.user_prompt}\nPrompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
    for candidate in response.candidates:
        messages.append(candidate.content)
    if response.function_calls:
        function_results=[]
        for function_call in response.function_calls:
            function_call_result=cf.call_function(function_call,args.verbose)
            
            if not function_call_result.parts:
                raise Exception("Content.parts is empty, it should'nt")
            else: 
                if function_call_result.parts[0].function_response == None:
                    raise Exception("Non function response")
                else: 
                    if function_call_result.parts[0].function_response.response == None:
                        raise Exception("Response missing from function_response")
                    else: 
                        function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        
        messages.append(types.Content(role="user", parts=function_results))
        return False
    else:       
        print(response.text)
        return True

if __name__ == "__main__":
    main()
