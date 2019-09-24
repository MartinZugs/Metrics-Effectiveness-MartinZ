# Import statements, just ordered dicts and requests for now
import requests
from collections import OrderedDict 

# Header with my token
headers = {"Authorization": }

# A simple function to use requests.post to make the API call. Note the json= section.
def run_query(query): 
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

        
# First query, this receives a list of all the commits with their dates and their OIDs      
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

# This is the second query to piggyback of the first one, what this does is the exact same thing as the first query, but it goes through all of the pages of the response
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

# An ordered dict of all of the commit dates and OIDs
dates_and_oids = OrderedDict([])

# Execute the query
result = run_query(first_query) 

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
    result = run_query(second_query % str(next_page))

    # Same as the above 
    for x in result["data"]["repository"]["object"]["history"]["nodes"]:
        dates_and_oids["'" + x["committedDate"] + "'"] = str(x["oid"])

    remaining_rate_limit = result["data"]["rateLimit"]["remaining"] 
    print("Remaining rate limit - {}".format(remaining_rate_limit))

    next_page = result["data"]["repository"]["object"]["history"]["pageInfo"]["endCursor"]

# Prints the ordered dict
for x in dates_and_oids:
    print(x)
    print(dates_and_oids[x])

