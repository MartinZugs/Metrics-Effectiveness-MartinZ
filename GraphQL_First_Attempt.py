# An example to get the remaining rate limit using the Github GraphQL API.

import requests
from collections import OrderedDict 

headers = {"Authorization": }


def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

        
# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
first_query = """
{
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
  
  repository(owner: "CornellNLP" name:"Cornell-Conversational-Analysis-Toolkit"){

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

#object(oid:"03cd07458a24b2241aebb27b0ea5219a44cf151a"){
#      ... on Commit{
#        oid
#        tree{
#          entries{
#            name
#            object{
#              ... on Blob{
#                text
#              }
#            }
#          }
#        }
#      }
#    }

second_query = """
{
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
  
  repository(owner: "CornellNLP" name:"Cornell-Conversational-Analysis-Toolkit"){

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

dates_and_oids = OrderedDict([])

result = run_query(first_query) # Execute the query

for x in result["data"]["repository"]["object"]["history"]["nodes"]:
    dates_and_oids["'" + x["committedDate"] + "'"] = str(x["oid"])

next_page = result["data"]["repository"]["object"]["history"]["pageInfo"]["endCursor"]

remaining_rate_limit = result["data"]["rateLimit"]["remaining"] # Drill down the dictionary
print("Remaining rate limit - {}".format(remaining_rate_limit))


while next_page:
    result = run_query(second_query % str(next_page))

    for x in result["data"]["repository"]["object"]["history"]["nodes"]:
        dates_and_oids["'" + x["committedDate"] + "'"] = str(x["oid"])

    remaining_rate_limit = result["data"]["rateLimit"]["remaining"] # Drill down the dictionary
    print("Remaining rate limit - {}".format(remaining_rate_limit))

    next_page = result["data"]["repository"]["object"]["history"]["pageInfo"]["endCursor"]

for x in dates_and_oids:
    print(x)
    print(dates_and_oids[x])

