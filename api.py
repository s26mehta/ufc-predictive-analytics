import pyodbc
from flask import Flask, jsonify, request, abort
import json


app = Flask(__name__)

def database_connection():
    server = 'ufcserve.database.windows.net'
    database = 'ufcDB'
    username = 's26mehta'
    password = 'Syde223@'
    driver = '{ODBC Driver 13 for SQL Server}'
    cnxn = pyodbc.connect(
        'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
        ';PWD=' + password)
    cursor = cnxn.cursor()
    cursor.execute("Insert into users(password, first_name, last_name, email, user_name) VALUES ('password', 'Sam', 'Gibson', 'sam@gmail.com', 'samg');")

    cnxn.commit()
    # row = cursor.fetchone()
    # if row:
    #     print row

    cursor.close()
    cnxn.close()




@app.route('/api/add_user', methods=['POST'])
def add_user():
    if not request.json:
        abort(400)

    statement = "Insert into Users(username, first_name, last_name, email, password) " \
                "VALUES (%s, %s, %s, %s, %s)" % (request.json['username'], request.json['first_name'],
                                                 request.json['last_name'], request.json['email'],
                                                 request.json['password'])



if __name__ == '__main__':
    # app.run(debug=True)
    database_connection()
