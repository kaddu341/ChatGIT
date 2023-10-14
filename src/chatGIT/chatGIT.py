import openai
import json
import sys
import subprocess
def setup():
    api_key = ''

    try:
        with open("config.ini", "r") as configfile:
            api_key = configfile.read()
    except:
        print("No ChatGPT API key found. Enter API key:")
        api_key = input("Please enter your API key")

        with open("config.ini", "w") as configfile:
            configfile.write(api_key)
    return api_key

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
def run_conversation(user_input):
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": user_input}]
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
    return response_message

def main():
    api_key = ''
    try:
        with open("config.txt", "r") as configfile:
            api_key = configfile.read()
    except:
        print("No ChatGPT API key found. Enter API key:")
        api_key = input("Please enter your API key")

        with open("config.txt", "w") as configfile:
            configfile.write(api_key)
    
    # set API key
    openai.api_key = api_key

    user_input = ''
    for i in range(1,len(sys.argv)):
        user_input += sys.argv[i] + ' '
    


    output = run_conversation(user_input)
    print_statement = '\033[94m'
    for i in output:
        for j in i:
            print_statement += j + " "
        print_statement += "\n"
    print_statement += '\033[0m'
    print()
    print(print_statement)

    print("Are these commands okay to execute? (y/n)", end=" ")
    confirmation = input()

    if 'y' in confirmation:
        try:
            for command in output:                
                subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f'Command {e.cmd} failed with error {e.returncode}')
    else:
        exit()
    
if __name__ == "__main__":
    main()


