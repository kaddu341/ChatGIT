import json

samples = [
"""push [FILE].xyz to github with the commit message "Hello World" """,

"""
git add [FILE].xyz
git commit text.txt -m "Hello World"
git push
""",

"""push the file text.txt to my repo with the message "Hola" """,

"""
git add text.txt
git commit text.txt -m "Hola"
git push
""",

"""push myprogram.py, message is "My first commit" """,

"""
git add myprogram.py
git commit myprogram.py -m "My first commit"
git push
""",

"""push somefile.cpp to github w/ msg "Finished for today" """,

"""
git add somefile.cpp
git commit somefile.cpp -m "Finished for today"
git push
""",

"""push all my changes to github""",

"""
git add .
git commit text.txt -m "Added all changes"
git push
""",

"""commit all my changes""",

"""
git commit -a -m "Committed all changes"
""",

"""pull changes from repo""",

"""
git pull
""",

"""switch to a new branch called my_branch_name""",

"""
git checkout -b my_branch_name
""",

"""show current status""",

"""
git status
""",

"""add my name to git config""",

"""
what is your name?
""",

"""first last""",

"""git config --global user.name "first last" """,

"""add my email to git config""",

"""what's your email?""",

"""someone@example.com""",

"""git config --global user.email “someone@example.com”""",

"""make the git command line prettier""",

"""git config --global color.ui auto""",

"""clone my repo into the local folder""",

"""what's the URL of your repo?""",

"""https://github.com/mrcomputernerd/coolprojecT.git""",

"""git clone https://github.com/mrcomputernerd/coolprojecT.git""",

"""show me a list of files in the staging area""",

"""git ls-files""",

"""go back to the previous commit""",

"""git reset""",

"""show me all branches in this project""",

"""git branch""",

"""switch to xyz branch""",

"""git checkout xyz""",

"""merge abc into this branch""",

"""git merge abc""",

"""make a new branch""",

"""what is the name of your branch?""",

"""awwab""",

"""git branch awwab""",

"""show me all commits""",

"""git log""",

"""show me what have I just changed in my files?""",

"""git diff""",

"""show me the differences in files in the staging area""",

"""git diff --staged""",

"""temporarily store my changes""",

"""git stash""",

"""list the changes I have stashed""",

"""git stash list""",

"""discard changes from the top of the stash""",

"""git stash drop""",

"""get the change at the top of the stash""",

"""git stash pop""",
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
            git_info = ["git add " + identifier, 'git commit -m "' + data + '"', 'git push']
        case "push-all":
            git_info = ['git commit -a -m "' + data + '"', 'git push']
        case "pull":
            git_info = ["git pull"]
        case "add":
            git_info = ["git add " + identifier]
        case "add-all":
            git_info = ["git add ."]
        case "commit-all":
            git_info = ['git commit -a -m "' + data + '"']
        case "commit":
            git_info = ['git commit -m "' + data + '"']
        case "initialize":
            git_info = ["git init"]
        case "clone":
            git_info = ["git clone " + data]
        case "set-name":
            git_info = ['git config global user.name "' + data + '"']
        case "set-email":
            git_info = ['git config global user.email "' + data + '"']
        case "set-color":
            git_info = ['git config --global color.ui auto']
        case "show-status":
            git_info = ["git status"]
        case "reset-commit":
            git_info = ['git reset']
        case "show-changes":
            git_info = ['git diff']
        case "show-staged-changes":
            git_info = ["git diff --staged"]
        case "list-branches":
            git_info = ['git branch']
        case "new-branch":
            git_info = ['git branch ' + identifier]
        case "switch-new-branch":
            git_info = ['git checkout -b ' + identifier]
        case "switch-branch":
            git_info = ['git checkout' + identifier]
        case "merge":
            git_info = ['git merge ' + identifier]
        case "show-commits":
            git_info = ['git log']
        case "stash":
            git_info = ['git stash']
        case "show-stash":
            git_info = ['git stash list']
        case "discard-stash":
            git_info = ['git stash drop']
        case "get-stash-top":
            git_info = ['git stash pop']
    
    return json.dumps(git_info)