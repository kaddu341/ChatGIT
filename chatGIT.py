#imports
import openai
import json
import re
import subprocess
from termcolor import cprint
from colorama import Fore, init
from sample_responses import generate_git_commands, samples

init() #for colorama

#user-AI conversation, adapted from https://platform.openai.com/docs/guides/gpt/function-calling
def run_conversation(user_input):
    #build a sample list of messages
    messages=[
        {"role": "system", "content": "Generate a series of git commands based on the user's input. Only use the functions you have been provided with."},
        {"role": "user", "content": samples[0]},
        {"role": "assistant", "content": samples[1]},
        {"role": "user", "content": samples[2]},
        {"role": "assistant", "content": samples[3]},
        {"role": "user", "content": samples[4]},
        {"role": "assistant", "content": samples[5]},
        {"role": "user", "content": samples[6]},
        {"role": "assistant", "content": samples[7]},
        {"role": "user", "content": samples[8]},
        {"role": "assistant", "content": samples[9]},
        {"role": "user", "content": samples[10]},
        {"role": "assistant", "content": samples[11]},
        {"role": "user", "content": samples[12]},
        {"role": "assistant", "content": samples[13]},
        {"role": "user", "content": samples[14]},
        {"role": "assistant", "content": samples[15]},
        {"role": "user", "content": samples[16]},
        {"role": "assistant", "content": samples[17]},
        {"role": "user", "content": samples[18]},
        {"role": "assistant", "content": samples[19]},
        {"role": "user", "content": samples[20]},
        {"role": "assistant", "content": samples[21]},
        {"role": "user", "content": samples[22]},
        {"role": "assistant", "content": samples[23]},
        {"role": "user", "content": samples[24]},
        {"role": "assistant", "content": samples[25]},
        {"role": "user", "content": samples[26]},
        {"role": "assistant", "content": samples[27]},
        {"role": "user", "content": samples[28]},
        {"role": "assistant", "content": samples[29]},
        {"role": "user", "content": samples[30]},
        {"role": "assistant", "content": samples[31]},
        {"role": "user", "content": samples[32]},
        {"role": "assistant", "content": samples[33]},
        {"role": "user", "content": samples[34]},
        {"role": "assistant", "content": samples[35]},
        {"role": "user", "content": samples[36]},
        {"role": "assistant", "content": samples[37]},
        {"role": "user", "content": samples[38]},
        {"role": "assistant", "content": samples[39]},
        {"role": "user", "content": samples[40]},
        {"role": "assistant", "content": samples[41]},
        {"role": "user", "content": samples[42]},
        {"role": "assistant", "content": samples[43]},
        {"role": "user", "content": samples[44]},
        {"role": "assistant", "content": samples[45]},
        {"role": "user", "content": samples[46]},
        {"role": "assistant", "content": samples[47]},
        {"role": "user", "content": samples[48]},
        {"role": "assistant", "content": samples[49]},
        {"role": "user", "content": samples[50]},
        {"role": "assistant", "content": samples[51]},
        {"role": "user", "content": samples[52]},
        {"role": "assistant", "content": samples[53]},
        {"role": "user", "content": samples[54]},
        {"role": "assistant", "content": samples[55]},
        {"role": "user", "content": samples[56]},
        {"role": "assistant", "content": samples[57]},
        {"role": "user", "content": samples[58]},
        {"role": "assistant", "content": samples[59]},
        {"role": "user", "content": user_input}
    ]
    
    # Step 1: send the conversation and available functions to GPT
    functions = [
        {
            "name": "generate_git_commands",
            "description": "get a list of the git commands required to achieve a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "enum": ["push", "push-all", "pull", "add", "add-all", "commit-all", "commit", "initialize", "clone", "set-name", "set-email", "set-color", "show-status", "reset-commit", "show-changes", "show-staged-changes", "list-branches", "new-branch", "switch-new-branch", "switch-branch", "merge", "show-commits", "stash", "show-stash", "discard-stash", "get-stash-top"],
                        "description": "The intended task to be achieved",
                    },
                    "identifier": {
                        "type": "string",
                        "description": "The name of the file or branch",
                    },
                    "data": {
                        "type": "string",
                        "description": "A name, email, URL, or an optional commit message",
                    },
                },
                "required": ["task"],
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
            identifier=function_args.get("identifier"),
            data=function_args.get("data"),
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
        return second_response["choices"][0]["message"]["content"]
    else:
        return response_message["content"]

def parse_output(output: str):
    # Define a regular expression pattern to match words between backticks
    backtick_pattern = r'`([^`]+)`'

    git_cmd_list = []
    #single line
    if len(output.splitlines()) == 1:
        if "git" in output:
            git_cmd_list = [output.strip()]
    else: #multiline
        if "`" in output:
            git_cmd_list = re.findall(backtick_pattern, output)

    cprint('\n'+output.replace("`", ""), 'green', attrs=['bold'])
    return git_cmd_list

def main():
    api_key = ''
    try:
        with open("config.txt", "r") as configfile:
            api_key = configfile.read()
    except:
        cprint("No ChatGPT API key found. Enter API key: ", 'magenta')
        api_key = input("Please enter your API key")

        with open("config.txt", "w") as configfile:
            configfile.write(api_key)
    
    # set API key
    openai.api_key = api_key

    cprint("ChatGIT version 0.01\nWhat do you want to do? (0 to exit)", 'magenta')
    user_input = str(input(Fore.YELLOW))

    while user_input != "0":
        output = str(run_conversation(user_input))
        git_commands = parse_output(output=output)

        if len(git_commands) != 0:
            choice = ""
            while choice != "y" and choice != "n":
                cprint("\nAre you ok with these commands to be executed? (y/n)", 'magenta', end = " ",)
                choice = str(input(Fore.YELLOW))
                try:
                    choice = choice.lower()
                except:
                    cprint("Invalid input", 'red', attrs=['bold'])
                
                if choice == "y":
                    for cmd in git_commands:
                        running_list = cmd.split()
                        subprocess.run(running_list)
                elif choice == "n":
                    cprint("Operation aborted", 'magenta')
                else:
                    cprint("Invalid input", 'red', attrs=['bold'])
        
        print()
        user_input = str(input(Fore.YELLOW))

if __name__ == "__main__":
    main()