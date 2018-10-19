# This script pulls from a job website and stores positions into a database. If there is a new posting it notifies the user.
# CNA 330
# Bill Erhard, wherhard@student.rtc.edu
import mysql.connector
import sys
import json
import urllib.request
import os
import time


# Connect to database
def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                   host='127.0.0.1',
                                   database='cna330')
    return conn


# Create the table structure
def create_tables(cursor, table):
    cursor.execute(f"DROP TABLE {table}")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INT PRIMARY KEY, post_date TEXT, title TEXT, location "
                   f"TEXT, full_part TEXT, description TEXT, apply_info TEXT, company TEXT, salary FLOAT, raw_message"
                   f" TEXT  );")
    return


# Query the database.
def query_sql(cursor, query):
    cursor.execute(query)
    return cursor


# Add a new job
def add_new_job(cursor, jobdetails):
    i = 0
    for job in jobdetails:
        # YYYY-MM-DD HH:MM:SS
        # github=Fri Oct 19 02:00:00 UTC 2018
        sql = f"INSERT INTO jobs (id, post_date, title, location, full_part) VALUES ({i}, '{job['created_at']}', '{job['title']}', '{job['location']}', '{job['type']}');"
        cursor.execute(sql)
        i += 1


def check_if_job_exists(cursor, jobdetails):
    ## Add your code here
    query = "SELECT"
    return query_sql(cursor, query)


def delete_job(cursor, jobdetails):
    ## Add your code here
    query = "UPDATE"
    return query_sql(cursor, query)


# Grab new jobs from a website
def fetch_new_jobs(arg_dict):
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
    query = "https://jobs.github.com/positions.json"  # ?" + "&location=seattle" # + "&description=" + description # Add arguments here
    jsonpage = 0
    try:
        contents = urllib.request.urlopen(query)
        response = contents.read()
        jsonpage = json.loads(response)



    except:
        print("whoops")
        pass
    return jsonpage


# Load a text-based configuration file
def load_config_file(filename):
    argument_dictionary = 0
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/FileIO.py
    rel_path = os.path.abspath(os.path.dirname(__file__))
    file_contents = 0
    try:
        file = open(filename, "r")
        file_contents = file.read()
    except FileNotFoundError:
        print("File not found, it will be created.")
        file = open(filename, "w")
        file.write("")
        file.close()

    # for row in file_contents:
    #     argument_dictionary += row
    ## Add in information for argument dictionary
    return argument_dictionary


# Main area of the code.
def jobhunt(arg_dict):
    # Fetch jobs from website
    jobpage = fetch_new_jobs(arg_dict)
    # print (jobpage)
    return jobpage
    ## Add your code here to parse the job page

    ## Add in your code here to check if the job already exists in the DB

    ## Add in your code here to notify the user of a new posting

    ## EXTRA CREDIT: Add your code to delete old entries


# Setup portion of the program. Take arguments and set up the script
def main():
    # Connect to SQL and get cursor
    fields = ["id", "post_date", "title", "location", "full_part", "description", "apply_info", "company", "salary",
              "raw_message"]
    conn = connect_to_sql()
    cursor = conn.cursor()
    arg_dict = load_config_file(sys.argv[1])

    create_tables(cursor, "jobs")
    # Load text file and store arguments into dictionary

    # config 1 tablename 2 location 3 0 4 description
    j = jobhunt(arg_dict)

    add_new_job(cursor, j)


# while(1):
#   jobhunt(arg_dict)
#   time.sleep(3600) # Sleep for 1h


if __name__ == '__main__':
    main()
