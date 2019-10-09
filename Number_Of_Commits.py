# Import statements, just ordered dicts and requests for now
import requests
from collections import OrderedDict
import re

# TODO - Make the data output into a CSV format #
# TODO - Number of collaborators #
# TODO - Pull requests, forks, branches #
# TODO - CSV will have rows be times and columns be metrics #
# TODO - Make python scripts for number of lines of code, commits, number of letters in code, and issues #

# Header with my token
headers = {"Authorization": "token "}

# A simple function to use requests.post to make the API call. Note the json= section.
def run_query(query): 
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

# A function that returns ther dates and oids of a github repo
def get_commit_dates_and_oids(dates_and_oids, un, rn):
    # Execute the query
    result = run_query(first_query % (un, rn)) 

    # Takes the response and adds the dates and OIDs to the ordered dict
    for x in result["data"]["repository"]["object"]["history"]["nodes"]:
        dates_and_oids["'" + x["committedDate"] + "'"] = str(x["oid"])

    # Gets the ID of the next page
    next_page = result["data"]["repository"]["object"]["history"]["pageInfo"]["endCursor"]

    # This gets the remaining number of calls that can be made
    remaining_rate_limit = result["data"]["rateLimit"]["remaining"] 
    print("Remaining rate limit - {}".format(remaining_rate_limit))

    # This loop goes through and paginates through all of the responses
    while next_page:
        # Calls the second query with the next call ID
        result = run_query(second_query % (un, rn, str(next_page)))

        # Same as the above 
        for x in result["data"]["repository"]["object"]["history"]["nodes"]:
            dates_and_oids["'" + x["committedDate"] + "'"] = str(x["oid"])

        remaining_rate_limit = result["data"]["rateLimit"]["remaining"] 
        print("Remaining rate limit - {}".format(remaining_rate_limit))

        next_page = result["data"]["repository"]["object"]["history"]["pageInfo"]["endCursor"]

    return dates_and_oids

def get_number_commits(dates_and_oids, un, rn):
    
    total = 0

    # Prints the ordered dict
    for x in dates_and_oids:

        # print(x)
        # print(dates_and_oids[x])

        total = total + 1

    return total

        
            

# First query, this receives a list of all the commits with their dates and their OIDs      
first_query = """
{
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
  
  repository(owner: "%s" name:"%s"){

    object(expression: "master") {
      ... on Commit {
        history {
          nodes {
            committedDate
            oid
          }
          pageInfo {
            endCursor
          }
        }
      }
    }
  }

}
"""

# This is the second query to piggyback of the first one, what this does is the exact same thing as the first query, but it goes through all of the pages of the response
second_query = """
{
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
  
  repository(owner: "%s" name:"%s"){

    object(expression: "master") {
      ... on Commit {
        history(after: "%s") {
          nodes {
            committedDate
            oid
          }
          pageInfo {
            endCursor
          }
        }
      }
    }
  }

}
"""

third_query = """
{
    rateLimit {
        limit
        cost
        remaining
        resetAt
      }

  repository(owner: "%s" name:"%s"){
    object(oid:"%s"){
      
      ... on Commit{
        oid
        tree{
          entries{
            name
            type
            oid
            object{
              ... on Tree {
                entries {
                oid
                name
                type
                    object{
                      ... on Tree {
                    entries {
                    oid
                    name
                    type
                        object{
                          ... on Tree {
                        entries {
                        oid
                        name
                        type}}
                        ... on Blob{
                            text
                          } 
                    }
                }\
                }
                      ... on Blob{
                        text
                      } 
                }
                  
              }
              }
              ... on Blob{
                text
              }
            }
          }
        }
      }
    }
  }
}

"""

# An ordered dict of all of the commit dates and OIDs
dates_and_oids = OrderedDict([])

# Allows the user to input their desired GitHub Repo information
username = input("Please input the username of the desired GitHub Repository owner: ")
repo_name = input("Please input the Repository name: ")

# Gets the dates and oids of all commits
dates_and_oids = get_commit_dates_and_oids(dates_and_oids, username, repo_name)

# Gets the number of letters
num_o_commits = get_number_commits(dates_and_oids, username, repo_name)

print (num_o_commits)

    
