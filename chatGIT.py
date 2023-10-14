#imports
import sys
import os
import configparser
import openai
import json


phrase = ''
for i in range(1,len(sys.argv)):
    phrase += sys.argv[i] + ' '

# Get the user's home directory
user_home = os.path.expanduser("~")

# Define the path to the configuration file
config_file_path = "config.ini"

# Read the API key from the configuration file
config = configparser.ConfigParser()
config.read(config_file_path)
api_key = config.get("API", "api_key")

if(api_key == 'none'):
    print("No ChatGPT API key found. Enter API key:")
    api_key = input("Please enter your API key")

with open(config_file_path, "w") as configfile:
    config.write(api_key)
    
# send "phrase to chatGPT"
openai.api_key = api_key

#function to be called by ChatGPT
def generate_git_commands(task: str, file: str, msg = ""):
    git_info = []
    match task:
        case "push":
            git_info = ["git add " + file, 'git commit -m "' + msg + '"', 'git push']
        case "pull":
            git_info = ["git pull"]
        case "add":
            git_info = ["git add " + file]
        case "commit":
            git_info = ['git commit -m "' + msg + '"']
        case "initialize":
            git_info = ["git init"]
        #case _:
    return json.dumps(git_info)

#user-AI conversation, adapted from https://platform.openai.com/docs/guides/gpt/function-calling
def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": phrase}]
    functions = [
        {
            "name": "generate_git_commands",
            "description": "get a list of the git commands required to achieve a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The intended task to be achieved",
                    },
                    "file": {
                        "type": "string",
                        "description": "The name of the file",
                    },
                    "msg": {
                        "type": "string",
                        "description": "An optional commit message",
                    },
                },
                "required": ["task", "file"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "generate_git_commands": generate_git_commands,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(
            task=function_args.get("task"),
            file=function_args.get("file"),
            msg=function_args.get("msg"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response
    else:
        return response_message

print(run_conversation())