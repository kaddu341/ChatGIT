import json

samples = [
"""push [FILE].xyz to github with the commit message "Hello World" """,

"""
git add [FILE].xyz\n
git commit text.txt -m "Hello World"\n
git push\n
""",

"""push the file text.txt to my repo with the message "Hola" """,

"""
git add text.txt\n
git commit text.txt -m "Hola"\n
git push\n
""",

"""push myprogram.py, message is "My first commit" """,

"""
git add myprogram.py\n
git commit myprogram.py -m "My first commit"\n
git push\n
""",

"""push somefile.cpp to github w/ msg "Finished for today" """,

"""
git add somefile.cpp\n
git commit somefile.cpp -m "Finished for today"\n
git push\n
""",

"""push all my changes to github""",

"""
git add .\n
git commit text.txt -m "Added all changes"\n
git push\n
""",

"""commit all my changes""",

"""
git commit -a -m "Committed all changes"\n
""",

"""pull changes from repo""",

"""
git pull\n
""",

"""switch to a new branch called my_branch_name""",

"""
git checkout -b my_branch_name\n
""",

"""show current status""",

"""
git status\n
""",

"""add my name to git config""",

"""
what is your name?
""",

"""first last""",

"""git config --global user.name "first last"\n""",

"""add my email to git config""",

"""what's your email?""",

"""someone@example.com""",

"""git config --global user.email “someone@example.com”\n""",

"""make the git command line prettier""",

"""git config --global color.ui auto\n""",

"""clone my repo into the local folder""",

"""what's the URL of your repo?""",

"""https://github.com/mrcomputernerd/coolprojecT.git""",

"""git clone https://github.com/mrcomputernerd/coolprojecT.git\n""",

"""show me a list of files in the staging area""",

"""git ls-files\n""",

"""go back to the previous commit""",

"""git reset\n""",

"""show me all branches in this project""",

"""git branch\n""",

"""switch to xyz branch""",

"""git checkout xyz\n""",

"""merge abc into this branch""",

"""git merge abc\n""",

"""make a new branch""",

"""what is the name of your branch?""",

"""awwab""",

"""git branch awwab\n""",

"""show me all commits""",

"""git log\n""",

"""show me what have I just changed in my files?""",

"""git diff\n""",

"""show me the differences in files in the staging area""",

"""git diff --staged\n""",

"""temporarily store my changes""",

"""git stash\n""",

"""list the changes I have stashed""",

"""git stash list\n""",

"""discard changes from the top of the stash""",

"""git stash drop\n""",

"""get the change at the top of the stash""",

"""git stash pop\n""",
                    ]

#function to be called by ChatGPT
def generate_git_commands(task: str, identifier: str = "", data = ""):
    git_info = []

    if identifier == None:
        identifier = ""
    if data == None:
        data = ""
    
    match task:
        case "push":
            git_info = ["git add " + identifier + '\n', 'git commit -m "' + data + '"\n', 'git push\n']
        case "push-all":
            git_info = ['git commit -a -m "' + data + '"\n', 'git push\n']
        case "pull":
            git_info = ["git pull\n"]
        case "add":
            git_info = ["git add " + identifier + '\n']
        case "add-all":
            git_info = ["git add .\n"]
        case "commit-all":
            git_info = ['git commit -a -m "' + data + '"\n']
        case "commit":
            git_info = ['git commit -m "' + data + '"\n']
        case "initialize":
            git_info = ["git init\n"]
        case "clone":
            git_info = ["git clone " + data + '\n']
        case "set-name":
            git_info = ['git config global user.name "' + data + '"\n']
        case "set-email":
            git_info = ['git config global user.email "' + data + '"\n']
        case "set-color":
            git_info = ['git config --global color.ui auto\n']
        case "show-status":
            git_info = ["git status\n"]
        case "reset-commit":
            git_info = ['git reset\n']
        case "show-changes":
            git_info = ['git diff\n']
        case "show-staged-changes":
            git_info = ["git diff --staged\n"]
        case "list-branches":
            git_info = ['git branch\n']
        case "new-branch":
            git_info = ['git branch ' + identifier + '\n']
        case "switch-new-branch":
            git_info = ['git checkout -b ' + identifier + '\n']
        case "switch-branch":
            git_info = ['git checkout' + identifier + '\n']
        case "merge":
            git_info = ['git merge ' + identifier + '\n']
        case "show-commits":
            git_info = ['git log\n']
        case "stash":
            git_info = ['git stash\n']
        case "show-stash":
            git_info = ['git stash list\n']
        case "discard-stash":
            git_info = ['git stash drop\n']
        case "get-stash-top":
            git_info = ['git stash pop\n']
    
    return json.dumps(git_info)