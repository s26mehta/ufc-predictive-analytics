import pyodbc
from flask import Flask, jsonify, request, abort
import json


app = Flask(__name__)

server = 'ufcserve.database.windows.net'
database = 'ufcDB'
username = 's26mehta'
password = 'Syde223@'
driver = '{ODBC Driver 13 for SQL Server}'

@app.route('/api/sign_up', methods=['POST'])
def sign_up():
    if not request.json:
        abort(400)
    try:
        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
            ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("Insert into users(user_name, first_name, last_name, email, password) " \
                    "VALUES ('%s', '%s', '%s', '%s', '%s')" % (request.json['username'], request.json['first_name'],
                                                     request.json['last_name'], request.json['email'],
                                                     request.json['password']))
        cnxn.commit()
        cursor.execute("Select id from users where user_name = '%s' and email = '%s' and last_name = '%s'" % (request.json['username'], request.json['email'], request.json['last_name']))
        row = cursor.fetchone()
        print row
        cursor.execute("Insert into dashboards(user_id, fighters) " \
                       "VALUES ('%s', '%s')" % (row[0], '302601'))
        cnxn.commit()
        cursor.close()
        cnxn.close()
        return jsonify(success=True)
    except:
        return jsonify(success=False)


@app.route('/api/log_in', methods=['GET'])
def log_in():
    if not request.json:
        abort(400)
    try:
        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
            ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("Select user_name, password from users where user_name = '%s' and password = '%s'" % (request.json['username'], request.json['password']))
        row = cursor.fetchone()
        print row
        cnxn.commit()
        cursor.close()
        cnxn.close()
        if row[0] == request.json['username'] and row[1] == request.json['password']:
            return jsonify(success=True)
        else:
            return jsonify(success=False)
    except:
        return jsonify(success=False)



if __name__ == '__main__':
    app.run(debug=True)
