import re

astring = """`git add abc`
```git commit -m "Hello world"```
```
git push
```"""
def split_cmd(line: str):
    if '"' in line:
        alist = line[0:line.find('"')].strip().split()
        alist.append(line[line.find('"'):])
    else:
        alist = line.split()
    return alist

def parse_output(output: str):
    # Define a regular expression pattern to match words between backticks
    backtick_pattern = r'`([^`]+)`'

    git_cmd_list = []
    #single line
    if "`" in output:
        git_cmd_list = re.findall(backtick_pattern, output)
    #make sure the list consists of only git commands
    for cmd in git_cmd_list:
        if "git" not in cmd:
            git_cmd_list.remove(cmd)
    #print output
    #cprint('\n'+output.replace("`", ""), 'green', attrs=['bold'])
    print('\n'+output)
    git_cmd_list = [split_cmd(cmd) for cmd in git_cmd_list] #make a 2D array
    return git_cmd_list

for cmd in parse_output(astring):
    print(cmd)