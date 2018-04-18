import MySQLdb
from flask import Flask, jsonify, request, abort
import json


app = Flask(__name__)

server = 'ufcserve.database.windows.net'
database = 'ufcDB'
username = 's26mehta'
password = 'Syde223@'
driver = '{SQL Server}'
from sys import platform
if platform == "darwin":
    driver = '{ODBC Driver 13 for SQL Server}'

@app.route('/api/sign_up', methods=['POST'])
def sign_up():
    print(request.form)
    if not request.form:
        abort(400)
    try:
        cnxn = MySQLdb.connect(host="localhost", user="root", db="ufcDB")
        # cnxn = pyodbc.connect('DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = cnxn.cursor()
        print('Hi')
        print("Insert into users(user_name, first_name, last_name, email, password) " \
                    "VALUES ('%s', '%s', '%s', '%s', '%s')" % (request.form['user_name'], request.form['first_name'],
                                                     request.form['last_name'], request.form['email'],
                                                     request.form['password']))
        cursor.execute("Insert into users(user_name, first_name, last_name, email, password) " \
                    "VALUES ('%s', '%s', '%s', '%s', '%s')" % (request.form['user_name'], request.form['first_name'],
                                                     request.form['last_name'], request.form['email'],
                                                     request.form['password']))
        cnxn.commit()
        cursor.execute("Select id from users where user_name = '%s' and email = '%s' and last_name = '%s'" % (request.form['user_name'], request.form['email'], request.form['last_name']))
        row = cursor.fetchone()
        # print row
        cursor.execute("Insert into dashboards(user_id, fighters) " \
                       "VALUES ('%s', '%s')" % (row[0], '302601'))
        cnxn.commit()
        cursor.close()
        cnxn.close()
        return jsonify(success=True, user_id=row[0])
    except e as error:
        print('HIT')
        return jsonify(success=False)


@app.route('/api/log_in', methods=['POST'])
def log_in():
    if not request.form:
        abort(400)
    try:
        cnxn = MySQLdb.connect(host="localhost", user="root", db="ufcDB")
        # cnxn = pyodbc.connect(
        #     'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
        #     ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("Select id, user_name, password, first_name from users where user_name = '%s' and password = '%s'" % (request.form['user_name'], request.form['password']))
        row = cursor.fetchone()
        print(row)
        cnxn.commit()
        cursor.close()
        cnxn.close()
        if row[1] == request.form['user_name'] and row[2] == request.form['password']:
            return jsonify(success=True, user_id=row[0], first_name=row[3])
        else:
            return jsonify(success=False)
    except:
        return jsonify(success=False)

@app.route('/api/get_all_fighters', methods=['POST'])
def get_all_fighters():
    try:
        cnxn = MySQLdb.connect(host="localhost", user="root", db="ufcDB")
        # cnxn = pyodbc.connect(
        #     'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
        #     ';PWD=' + password)
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


@app.route('/api/get_fighter', methods=['POST', 'GET'])
def get_fighter():
    # print request.form
    if not request.form:
        abort(400)
    try:
        # print 'here'
        cnxn = MySQLdb.connect(host="localhost", user="root", db="ufcDB")
        # cnxn = pyodbc.connect(
        #     'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
        #     ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("Select * from fighters where id=%s" % request.form['id'])
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

@app.route('/api/get_dashboard', methods=['POST'])
def get_dashboard():
    # print request.form
    # print request.json
    if not request.form:
        abort(400)
    try:
        cnxn = MySQLdb.connect(host="localhost", user="root", db="ufcDB")

        # cnxn = pyodbc.connect(
        #     'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
        #     ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("Select * from dashboards where user_id='%s'" % request.form['user_id'])
        row1 = cursor.fetchone()
        # print 'here'

        # print row1
        res = []
        a = {
            'id' : row1[0],
            'fighters': row1[1],
            'user_id': row1[2]
        }
        res.append(a)
        all_fighters_id = a['fighters'].split(",")
        print(all_fighters_id)
        fighters = []
        for fighter in all_fighters_id:
            cursor.execute("Select * from fighters where id=%s" % fighter)
            row = cursor.fetchone()
            # print 'here'
            # print row
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
                       fighters = fighters)
    except:
        return jsonify(success=False)


@app.route('/api/dashboard/add_fighter', methods=['POST'])
def add_fighter():
    if not request.form:
        abort(400)
    try:
        cnxn = MySQLdb.connect(host="localhost", user="root", db="ufcDB")
        # cnxn = pyodbc.connect(
        #     'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
        #     ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("Select fighters from dashboards where user_id=%s" % request.form['user_id'])
        row = cursor.fetchone()
        old_fighters= row[0]
        add_fighters = request.form['fighter_id'].split(",")
        for fighter in add_fighters:
            old_fighters = old_fighters + ", " + fighter
        cursor.execute("Update dashboards set fighters = '%s' where user_id='%s'" % (old_fighters, request.form['user_id']))
        cnxn.commit()
        cursor.close()
        cnxn.close()
        return jsonify(success=True)
    except:
        return jsonify(success=False)


@app.route('/api/get_live_fight_data', methods=['POST'])
def get_live_fight_data():
    if not request.form:
        abort(400)
    try:
        cnxn = MySQLdb.connect(host="localhost", user="root", db="ufcDB")
        # cnxn = pyodbc.connect(
        #     'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
        #     ';PWD=' + password)
        cursor = cnxn.cursor()

        cursor.execute(
            "Select fighter1_id, fighter2_id from fights where id=%s" % request.form['fight_id'])
        row1 = cursor.fetchone()
        fighters = []
        b = {
            'fighter1_id': row1[0],
            'fighter2_id': row1[1]
        }
        fighters.append(b)

        cursor.execute("Select fight_id, fighter_id, round, knock_down_landed, total_strikes, distance_strikes, clinch_total_strikes, "
                       "ground_total_strikes, head_total_strikes, body_total_strikes, legs_total_strikes, "
                       "takedowns, submissions, reversals_landed, standups_landed "
                       "from live_fight_data where fight_id=%s" % request.form['fight_id'])
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
                       response = res,
                       fighters = fighters)
    except:
        return jsonify(success=False)

if __name__ == '__main__':
    app.run(debug=True)
