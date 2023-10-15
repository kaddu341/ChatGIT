import subprocess

astring = """git add output.txt
git commit -m "Updated output.txt"
git push
"""
arr = astring.splitlines()
def split_cmd(line: str):
    if '"' in line:
        alist = line[0:line.find('"')].strip().split()
        alist.append(line[line.find('"'):])
    else:
        alist = line.split()
    return alist

arr = [split_cmd(line) for line in arr]
print(arr)