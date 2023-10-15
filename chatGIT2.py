import re

def parse_output(output: str):
    # Define a regular expression pattern to match words between backticks
    backtick_pattern = r'`([^`]+)`'

    git_cmd_list = []
    #single line
    if len(output.splitlines()) == 1:
        if "git" in output:
            git_cmd_list = [output]
    else: #multiline
        if "`" in output:
            git_cmd_list = re.findall(backtick_pattern, output)
    print(output.replace("`", ""))
    return git_cmd_list

myinput = """
Here are the commands to push all your changes to GitHub:

1. `git add .` (to add all changes)
2. `git commit -m "origin"` (to commit changes with the message "origin")
3. `git push` (to push changes to GitHub)

Please make sure you are in the appropriate branch before executing these commands.
"""
alist = parse_output(myinput)
print(alist)