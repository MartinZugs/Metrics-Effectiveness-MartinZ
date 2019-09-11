from github import Github
import requests

r = requests.get("https://api.codetabs.com/v1/loc?github=CornellNLP/Cornell-Conversational-Analysis-Toolkit")

print(r.json())

for index in r.json():
    if(index["language"] == "Total"):
        print(index["linesOfCode"])

print(" ")

# First create a Github instance:

# using username and password
#g = Github("user", "password")

# or using an access token
g = Github("a17012578d9ae6ee791f5e79bd25a6e9e303b414")

# Github Enterprise with custom hostname
#g = Github(base_url="https://github.com/MartinZugs/super-happiness/api/v3", login_or_token="a17012578d9ae6ee791f5e79bd25a6e9e303b414")

# Then play with your Github objects:
#for repo in g.get_user().get_repos():
    #print (repo)

print(g.get_repo("CornellNLP/Cornell-Conversational-Analysis-Toolkit").name)

print(" ")

repo = g.get_repo("CornellNLP/Cornell-Conversational-Analysis-Toolkit")

print(repo.updated_at)

print(" ")

contents = repo.get_contents("")
for content_file in contents:
    print(content_file)
