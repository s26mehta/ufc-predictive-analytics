import pyodbc

server = 'ufcserve.database.windows.net'
database = 'ufcDB'
username = 's26mehta'
password = 'Syde223@'
driver = '{ODBC Driver 13 for SQL Server}'


def add_live_fight_data(fight_id, fighter_id, round_num, knock_down_landed, total_strikes, distance_strikes,
                    clinch_total_strikes, ground_total_strikes, head_total_strikes, body_total_strikes,
                    legs_total_strikes, takedowns, submissions, reversals_landed, standups_landed):
    try:
        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
            ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("Select * from live_fight_data where fight_id='%s' and fighter_id='%s' "
                       "and round='%s'" % (fight_id, fighter_id, round))

        row = cursor.fetchone()
        if row:
            cursor.execute("Update live_fight_data set knock_down_landed='%s', total_strikes='%s', "
                           "distance_strikes='%s', clinch_total_strikes='%s', ground_total_strikes='%s', "
                           "head_total_strikes='%s', body_total_strikes='%s', legs_total_strikes='%s', "
                           "takedowns='%s', submissions='%s', reversals_landed='%s', standups_landed='%s' where "
                           "fight_id = '%s', fighter_id='%s', round='%s'" % (knock_down_landed, total_strikes,
                                                                             distance_strikes, clinch_total_strikes,
                                                                             ground_total_strikes, head_total_strikes,
                                                                             body_total_strikes, legs_total_strikes,
                                                                             takedowns, submissions, reversals_landed,
                                                                             standups_landed, fight_id, fighter_id, round_num))
        else:
            cursor.execute("Insert into live_fight_data(fight_id, fighter_id, round, knock_down_landed, total_strikes, "
                           "distance_strikes, clinch_total_strikes, ground_total_strikes, head_total_strikes, "
                           "body_total_strikes, legs_total_strikes, takedowns, submissions, reversals_landed, "
                           "standups_landed) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', "
                           "'%s', '%s', '%s', '%s', '%s', '%s')" % (fight_id, fighter_id, round_num, knock_down_landed,
                                                                    total_strikes, distance_strikes, clinch_total_strikes,
                                                                    ground_total_strikes, head_total_strikes,
                                                                    body_total_strikes, legs_total_strikes,  takedowns,
                                                                    submissions, reversals_landed, standups_landed))

        cnxn.commit()
        cursor.close()
        cnxn.close()
        return True
    except:
        return False


print add_live_fight_data('286539', '535918', '1', '10', '10:20', '1:10', '1:10', '0:0', '20:25', '1:5', '1:5', '0', '0', '0', '0')