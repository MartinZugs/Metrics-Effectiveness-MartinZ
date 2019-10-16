# Import statements
import requests
from collections import OrderedDict
import re
from datetime import datetime
import csv

# TODO - Make the data output into a CSV format #
# TODO - Number of collaborators #
# TODO - Pull requests, forks, branches #
# TODO - CSV will have rows be times and columns be metrics #
# TODO - Make python scripts for number of lines of code, commits, number of letters in code, and issues #

# Header with my token
headers = {"Authorization": "token c5b4966c0daf383782193872bbf19a7990b96aa5"}

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

def get_closest_date(dates_and_oids, date):

    date_convert = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    
    for x in dates_and_oids:
        x = x.replace("T", " ")
        x = x.replace("Z", " ")
        x_day = datetime.strptime(x, "'%Y-%m-%d %H:%M:%S '")

        for y in dates_and_oids:
            y = y.replace("T", " ")
            y = y.replace("Z", " ")
            y_day = datetime.strptime(y, "'%Y-%m-%d %H:%M:%S '")
            
            if(x_day > date_convert and y_day < date_convert):
                return (y_day)
                
            elif(x_day < date_convert and y_day < date_convert):
                return (x_day)
            
def get_lines_of_code(dates_and_oids, un, rn, date):
    
    total = ""

    f = open("lines.csv", "w+")
    writer = csv.DictWriter(f, fieldnames=["date", "oid", "total"])
    writer.writeheader()

    # Prints the ordered dict
    for x in dates_and_oids:
        x_day = x.replace("T", " ")
        x_day = x_day.replace("Z", " ")
        x_day = datetime.strptime(x_day, "'%Y-%m-%d %H:%M:%S '")

        if (x_day == date):

            #print(x)
            #print(dates_and_oids[x])
            content = run_query(third_query % (un, rn, str(dates_and_oids[x])))

            remaining_rate_limit = content["data"]["rateLimit"]["remaining"] 
            print("Remaining rate limit - {}".format(remaining_rate_limit))
            
            for y in content['data']['repository']['object']['tree']['entries']:
                total = total + (y['object']['text'])

            print (total)
            print("END OF SECTION")
            print(total.count('\n'))
            f = open("lines.csv", "w+")
            writer.writerows([{"date": str(x_day), "oid": str(dates_and_oids[x]), "total": str(total.count('\n'))}])

    f.close()
    return total.count('\n')
            

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
date = input("Please input the date in 2019-09-25 06:10:01 format that you wish to pull code from: ")

# Gets the dates and oids of all commits
dates_and_oids = get_commit_dates_and_oids(dates_and_oids, username, repo_name)

# Gets the closest commit date to use to pull metrics from
closest_date = get_closest_date(dates_and_oids, date)
print(closest_date)

# Gets the number of letters
num_o_lines = get_lines_of_code(dates_and_oids, username, repo_name, closest_date)
print(num_o_lines)
    
