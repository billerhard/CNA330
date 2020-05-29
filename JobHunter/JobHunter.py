# This script pulls from a job website and stores positions into a database. If there is a new posting it notifies
# the user.
# CNA 330
# Bill Erhard, wherhard@student.rtc.edu
import json
import sqlite3
import sys
import urllib.request


def connect_to_sql():
    conn = sqlite3.connect("jobs.db")
    return conn


def create_tables(cursor, fields):
    query = '''CREATE TABLE IF NOT EXISTS jobs (%s TEXT, %s TEXT, %s TEXT, ''' \
            '''%s TEXT, %s TEXT, %s TEXT, %s TEXT, %s TEXT, %s TEXT, %s TEXT, %s TEXT);''' % tuple(fields)

    return cursor.execute(query)


def add_new_job(cursor, job_details):
    # https://stackoverflow.com/questions/7540803/escaping-strings-with-python-mysql-connector

    data = (job_details['id'], job_details['type'], job_details['url'], job_details['created_at'],
            job_details['company'], job_details['company_url'], job_details['location'], job_details['title'],
            job_details['description'], job_details['how_to_apply'], job_details['company_logo'])
    sql = "INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?,?,?,?);"

    cursor.execute(sql, data)


def check_if_job_exists(cursor, jobdetails):
    query = '''SELECT job_id FROM jobs WHERE job_id="%s";''' % (jobdetails['id'])
    cursor.execute(query)
    return cursor.fetchall()


def fetch_new_jobs(arg_dict, page):
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
    query = "https://jobs.github.com/positions.json?location=%s&description=%s&page=%s" % \
            (arg_dict[1], arg_dict[3], page)
    jsonpage = 0
    try:
        contents = urllib.request.urlopen(query)
        response = contents.read()
        jsonpage = json.loads(response)
    except:
        print("whoops")
        pass
    return jsonpage


def load_config_file(filename):
    argument_dictionary = ""
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/FileIO.py
    file_contents = 0
    try:
        file = open(filename, "r")
        file_contents = file.read()
    except FileNotFoundError:
        print("File not found, it will be created.")
        file = open(filename, "w")
        file.write("")
        file.close()

    for row in file_contents:
        argument_dictionary += row
    return argument_dictionary


def add_jobs_from_page(cursor, jobpage):
    for job in jobpage:
        if check_if_job_exists(cursor, job):
            continue
        add_new_job(cursor, job)


def jobhunt(cursor, arg_dict):
    page = 0
    jobpage = fetch_new_jobs(arg_dict, page)
    while True:
        if jobpage:
            add_jobs_from_page(cursor, jobpage)
            page += 1
            jobpage = fetch_new_jobs(arg_dict, page)
        else:
            break


def display_jobs(cursor):
    for job in cursor.execute('SELECT * FROM jobs;'):
        print(job)


def main():
    fields = ["job_id", "type", "url", "created_at", "company", "company_url", "location", "title", "description",
              "how_to_apply", "company_logo"]
    conn = connect_to_sql()
    cursor = conn.cursor()
    arg_dict = load_config_file(sys.argv[1]).split('\n')
    create_tables(cursor, fields)
    jobhunt(cursor, arg_dict)
    conn.commit()
    display_jobs(cursor)
    conn.close()


if __name__ == '__main__':
    main()
