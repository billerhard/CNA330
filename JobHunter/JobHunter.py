# This script pulls from a job website and stores positions into a database. If there is a new posting it notifies
# the user.
# CNA 330
# Bill Erhard, wherhard@student.rtc.edu
import mysql.connector
import sys
import json
import urllib.request
import os


def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                   host='127.0.0.1',
                                   database='cna330')
    return conn


def create_tables(cursor, table, fields):
    fields.insert(0, table)
    fields = tuple(fields)
    query = '''CREATE TABLE IF NOT EXISTS %s (%s INTEGER PRIMARY KEY AUTO_INCREMENT, %s TEXT, %s TEXT, %s TEXT, ''' \
            '''%s TEXT, %s TEXT, %s TEXT, %s TEXT, %s TEXT, %s TEXT, %s TEXT);''' % fields

    return query_sql(cursor, query)


def query_sql(cursor, query):
    cursor.execute(query)
    return cursor


def add_new_job(cursor, job_details):
    # https://stackoverflow.com/questions/7540803/escaping-strings-with-python-mysql-connector

    data = (job_details['id'], job_details['created_at'], job_details['title'], job_details['location'], job_details['type'], job_details['description'],
            job_details['how_to_apply'], job_details['company'], "Bookoo Bucks", str(job_details))
    sql = "INSERT INTO jobs (job_id, post_date, title, location, full_part, description, apply_info, company, " \
          "salary, raw_message) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); "


    cursor.execute(sql, data)


def check_if_job_exists(cursor, jobdetails):
    query = '''SELECT %s FROM %s WHERE %s="%s";''' % ("job_id", "jobs", "job_id", jobdetails['id'])
    cursor.execute(query)
    return cursor.fetchall()


def get_job_id(cursor, jobdetails):

    pass


def delete_job(cursor, jobdetails):
    job_id = get_job_id(cursor, jobdetails)
    query = '''DELETE FROM %s WHERE %s=%s''' % ("jobs", "id", job_id)
    return query_sql(cursor, query)


def fetch_new_jobs(arg_dict):
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
    query = "https://jobs.github.com/positions.json?location=%s&description=%s" % (arg_dict[1], arg_dict[3])
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

    for row in file_contents:
        argument_dictionary += row
    return argument_dictionary


def jobhunt(cursor, arg_dict):
    jobpage = fetch_new_jobs(arg_dict)
    for job in jobpage:
        if check_if_job_exists(cursor, job):
            continue
        add_new_job(cursor, job)
    return jobpage


def main():
    fields = ["id", "job_id", "post_date", "title", "location", "full_part", "description", "apply_info", "company",
              "salary", "raw_message"]
    conn = connect_to_sql()
    cursor = conn.cursor()
    arg_dict = load_config_file(sys.argv[1]).split('\n')
    create_tables(cursor, arg_dict[0], fields)
    jobhunt(cursor, arg_dict)


if __name__ == '__main__':
    main()
