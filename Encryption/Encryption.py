# Encrypts some stuff in a database
# wherhard@student.rtc.edu
# Bill Erhard CNA 330 Fall 2018
import mysql.connector


def main():
    conn = mysql.connector.connect(user='root', password='',
                                   host='127.0.0.1', database='cna330')
    cursor = conn.cursor()
    # cursor.execute('''CREATE TABLE IF NOT EXISTS encrypted (id INTEGER PRIMARY
    # KEY AUTO_INCREMENT, username TEXT, password TEXT, credit_card TEXT,
    # ssn TEXT);''')
    #
    cursor.execute('''INSERT INTO encrypted(username, password, credit_card, ssn
    ) VALUES ("zrubin", SHA2("correcthorsebatterystaple", 256), "4001 4246 1234 
    5678",
    "000-00-0000");''')

    # cursor.execute('''SELECT SHA2('', 256);''')
    # result = cursor.fetchall()
    # print(result)

    conn.commit()
    conn.close


if __name__ == '__main__':
    main()
