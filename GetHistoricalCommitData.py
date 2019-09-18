import requests
import json
from datetime import datetime
timestamp = 1545730073
dt_object = datetime.fromtimestamp(timestamp)

####
# inputs
####
username = 'MartinZugs'

# from https://github.com/user/settings/tokens
token = '785adec08c81ac47883dc8ce1d5d56aab8738c4e'

commits_url = 'https://api.github.com/repos/CornellNLP/Cornell-Conversational-Analysis-Toolkit/stats/contributors'
add_delete_url = 'https://api.github.com/repos/CornellNLP/Cornell-Conversational-Analysis-Toolkit/stats/code_frequency'

# create a re-usable session object with the user creds in-built
gh_session = requests.Session()
gh_session.auth = (username, token)

# get the list of commits in the past year
r = gh_session.get(commits_url).json()

# print the total commits per person per week for the last year
for commit in r:
    print (commit)

chosen_date = input("Put in a date in (2019-08-24) this format and I will return the amount of additions, deletions, and net change for the week: ")
c_d = datetime.strptime(chosen_date, '%Y-%m-%d')

# get the list of total additions and deletions per week
r = gh_session.get(add_delete_url).json()

# print all of the additions and deletions
for a_d in r:

    date = datetime.fromtimestamp(a_d[0])
    #print(datetime.fromtimestamp(a_d[0]))
    additions = a_d[1]
    #print(a_d[1])
    deletions = a_d[2]
    #print(a_d[2])
    #print((c_d - date).days)
    
    if ((c_d - date).days > -7):
        if ((c_d - date).days < 0):
            print("Additions: " + str(additions))
            print("Deletions: " + str(deletions))
            print("Difference: " + str(additions - deletions))
        
