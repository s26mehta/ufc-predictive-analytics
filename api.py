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
                    "VALUES ('%s', '%s', '%s', '%s', '%s')" % (request.json['user_name'], request.json['first_name'],
                                                     request.json['last_name'], request.json['email'],
                                                     request.json['password']))
        cnxn.commit()
        cursor.execute("Select id from users where user_name = '%s' and email = '%s' and last_name = '%s'" % (request.json['user_name'], request.json['email'], request.json['last_name']))
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
        cursor.execute("Select user_name, password from users where user_name = '%s' and password = '%s'" % (request.json['user_name'], request.json['password']))
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

@app.route('/api/get_all_fighters', methods=['GET'])
def get_all_fighters():
    try:
        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
            ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("Select * from fighters")
        row = cursor.fetchone()
        res = []
        while row:
            a = {
                'id' : row[0],
                'first_name': row[1],
                'last_name': row[2],
                'nickname': row[3],
                'record': row[4] + "-" + row[5] + "-" +row[6],
                'rank': row[7],
                'pfp_rank': row[8],
                'profile_image': row[9],
                'fighter_status': row[10],
                'weight_class': row[11],
                'left_image': row[12],
                'right_image': row[13],
                'reach': row[14],
                'weight': row[15],
                'height': row[16],
                'submission_avg': row[17],
                'avg_fight_time': row[18],
                'slpm': row[19],
                'takedown_avg': row[20],
                'sapm': row[21],
                'striking_defense': row[22],
                'takedown_accuracy': row[23],
                'takedown_defense': row[24],
                'kd_avg': row[25],
                'striking_accuracy': row[26]
            }
            res.append(a)
            row = cursor.fetchone()
        cnxn.commit()
        cursor.close()
        cnxn.close()
        return jsonify(success=True,
                       response = res)
    except:
        return jsonify(success=False)

@app.route('/api/get_fighter', methods=['GET'])
def get_fighter():
    if not request.json:
        abort(400)
    try:
        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
            ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("Select * from fighters where id=%s" % request.json['id'])
        row = cursor.fetchone()
        res = []
        a = {
            'id' : row[0],
            'first_name': row[1],
            'last_name': row[2],
            'nickname': row[3],
            'record': row[4] + "-" + row[5] + "-" +row[6],
            'rank': row[7],
            'pfp_rank': row[8],
            'profile_image': row[9],
            'fighter_status': row[10],
            'weight_class': row[11],
            'left_image': row[12],
            'right_image': row[13],
            'reach': row[14],
            'weight': row[15],
            'height': row[16],
            'submission_avg': row[17],
            'avg_fight_time': row[18],
            'slpm': row[19],
            'takedown_avg': row[20],
            'sapm': row[21],
            'striking_defense': row[22],
            'takedown_accuracy': row[23],
            'takedown_defense': row[24],
            'kd_avg': row[25],
            'striking_accuracy': row[26]
        }
        res.append(a)

        cnxn.commit()
        cursor.close()
        cnxn.close()
        return jsonify(success=True,
                       response = res)
    except:
        return jsonify(success=False)

@app.route('/api/get_dashboard', methods=['GET'])
def get_dashboard():
    if not request.json:
        abort(400)
    try:
        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
            ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("Select * from dashboards where user_id=%s" % request.json['user_id'])
        row1 = cursor.fetchone()
        print row1
        res = []
        a = {
            'id' : row1[0],
            'fighters': row1[1],
            'user_id': row1[2]
        }
        res.append(a)
        all_fighters_id = a['fighters'].split(",")
        fighters = []
        for fighter in fighters:
            cursor.execute("Select * from fighters where id=%s" % fighter)
            row = cursor.fetchone()
            x = {
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'nickname': row[3],
                'record': row[4] + "-" + row[5] + "-" + row[6],
                'rank': row[7],
                'pfp_rank': row[8],
                'profile_image': row[9],
                'fighter_status': row[10],
                'weight_class': row[11],
                'left_image': row[12],
                'right_image': row[13],
                'reach': row[14],
                'weight': row[15],
                'height': row[16],
                'submission_avg': row[17],
                'avg_fight_time': row[18],
                'slpm': row[19],
                'takedown_avg': row[20],
                'sapm': row[21],
                'striking_defense': row[22],
                'takedown_accuracy': row[23],
                'takedown_defense': row[24],
                'kd_avg': row[25],
                'striking_accuracy': row[26]
            }
            fighters.append(x)
        cnxn.commit()
        cursor.close()
        cnxn.close()
        return jsonify(success=True,
                       dasboard = res,
                       fighters=fighters)
    except:
        return jsonify(success=False)


@app.route('/api/dashboard/add_fighter', methods=['GET'])
def add_fighter():
    if not request.json:
        abort(400)
    try:
        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
            ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("Select fighters from dashboards where user_id=%s" % request.json['user_id'])
        row = cursor.fetchone()
        old_fighters= row[0]
        add_fighters = request.json['fighters'].split(",")
        for fighter in add_fighters:
            old_fighters = old_fighters + ", " + fighter
        cursor.execute("Update dashboards set fighters = '%s' where user_id='%s'" % (old_fighters, request.json['user_id']))
        cnxn.commit()
        cursor.close()
        cnxn.close()
        return jsonify(success=True)
    except:
        return jsonify(success=False)

@app.route('/api/get_live_fight_data', methods=['GET'])
def live_fight_data():
    if not request.json:
        abort(400)
    try:
        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
            ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("Select fight_id, fighter_id, round, knock_down_landed, total_strikes, distance_strikes, clinch_total_strikes, "
                       "ground_total_strikes, head_total_strikes, body_total_strikes, legs_total_strikes, "
                       "takedowns, submissions, reversals_landed, standups_landed "
                       "from live_fight_data where fight_id=%s" % request.json['fight_id'])
        row = cursor.fetchone()
        res = []
        while row:
            a = {
                'fight_id': row[0],
                'fighter_id': row[1],
                'round': row[2],
                'knock_down' : row[3],
                'total_strikes': row[4],
                'distance_total_strikes': row[5],
                'clinch_total_strikes': row[6],
                'ground_total_strikes': row[7],
                'head_total_strikes': row[8],
                'body_total_strikes': row[9],
                'legs_total_strikes': row[10],
                'takedowns': row[11],
                'submissions': row[12],
                'reversals_landed': row[13],
                'standups_landed': row[14]
            }
            res.append(a)
            row = cursor.fetchone()

        cnxn.commit()
        cursor.close()
        cnxn.close()
        return jsonify(success=True,
                       response = res)
    except:
        return jsonify(success=False)


if __name__ == '__main__':
    app.run(debug=True)

