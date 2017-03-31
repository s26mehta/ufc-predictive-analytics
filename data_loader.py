import pyodbc
import urllib2
import simplejson as json
import flask
import datetime

server = 'ufcserve.database.windows.net'
database = 'ufcDB'
username = 's26mehta'
password = 'Syde223@'
driver= '{ODBC Driver 13 for SQL Server}'

def load_fighters():
    fighters = json.load(urllib2.urlopen("http://ufc-data-api.ufc.com/api/v3/fighters"))
    for fighter in fighters:
        print fighter
        id = str(fighter['id'])
        try:
            nickname = str(fighter['nickname'] if fighter['rank'] != None else 'null')
            try:
                nickname = nickname.replace("'", "''")

            except:
                nickname = nickname
        except:
            nickname = 'null'
        wins = str(fighter['wins'])
        losses = str(fighter['losses'])
        draws = str(fighter['draws'])
        rank = str(fighter['rank'] if fighter['rank'] != None else 'null')
        pfp_rank = str(fighter['pound_for_pound_rank'] if fighter['pound_for_pound_rank']!= None else 'null')
        first_name = str(fighter['first_name'])
        try:
            last_name = str(fighter['last_name'])
        except:
            last_name = fighter['last_name'].encode('utf-8')
        profile_image = str(fighter['profile_image'])
        fighter_status = str(fighter['fighter_status'])
        weight_class = str(fighter['weight_class'])
        try:
            right_image = str(fighter['right_full_body_image'])
        except:
            right_image = 'null'
        try:
            left_image = str(fighter['left_full_body_image'])
        except:
            left_image = 'null'
        reach = '0'
        weight = '0'
        height = '0'
        avg_fight_time = '0'
        kd_avg = '0'
        slpm = '0'
        striking_accuracy = '0'
        sapm = '0'
        striking_defense = '0'
        takedown_avg = '0'
        takedown_accuracy = '0'
        takedown_defense = '0'
        submission_avg = '0'

        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
            ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("Insert into fighters(id, first_name, last_name, nickname, wins, losses, draws, rank, "
                       "pfp_rank, profile_image, fighter_status, weight_class, right_image, left_image, reach, "
                       "weight, height, avg_fight_time, kd_avg, slpm, striking_accuracy, sapm, striking_defense, "
                       "takedown_avg, takedown_accuracy, takedown_defense, submission_avg) VALUES ('"+id+
                       "', '"+first_name+"', '"+last_name+"', '"+nickname+"', '"+wins+"', '"+losses+"', '"+draws+"', '"+rank+
                       "', '"+pfp_rank+"', '"+profile_image+"', '"+fighter_status+"', '"+weight_class+"', '"+right_image+
                       "', '"+left_image+"', '"+reach+"', '"+weight+"', '"+height+"', '"+avg_fight_time+"', '"+kd_avg+"', '"+slpm+
                       "', '"+striking_accuracy+"', '"+sapm+"', '"+striking_defense+"', '"+takedown_avg+"', '"+takedown_accuracy+
                       "', '"+takedown_defense+"', '"+submission_avg+"')")

        cnxn.commit()
        cursor.close()
        cnxn.close()


def load_events():
    events = json.load(urllib2.urlopen("http://ufc-data-api.ufc.com/api/v3/events"))

    for i in range(len(events)):
        print events[i]
        id = str(events[i]['id'])
        if events[i]['event_time_text'] != '':
            event_date = datetime.datetime.strptime(events[i]['event_date'], '%Y-%m-%dT%H:%M:%SZ')
            try:
                event_time = int(events[i]['event_time_text'][:2])
            except:
                event_time = int(events[i]['event_time_text'][:1])
            event_date = event_date.replace(hour=event_time)
        else:
            event_date = datetime.datetime.strptime(events[i]['event_date'], '%Y-%m-%dT%H:%M:%SZ')

        base_title = events[i]['base_title'] if events[i]['base_title'] != None else 'null'
        title_tag_line = events[i]['title_tag_line'] if events[i]['title_tag_line'] != None else 'null'
        subtitle = events[i]['subtitle'] if events[i]['subtitle'] != None else 'null'
        try:
            subtitle = subtitle.replace("'", "''")
        except:
            subtitle = subtitle
        event_status = events[i]['event_status']
        last_modified = datetime.datetime.strptime(events[i]['event_date'], '%Y-%m-%dT%H:%M:%SZ')
        url_name = events[i]['url_name']

        try:
            main_fighter_1 = str(events[i]['main_event_fighter1_id'])
        except:
            main_fighter_1 = 'null'
        try:
            main_fighter_2 = str(events[i]['main_event_fighter2_id'])
        except:
            main_fighter_2 = 'null'

        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
            ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("Insert into events(id, event_time, base_title, title_tag_line, subtitle, event_status, "
                       "last_modified, url_name, main_fighter_1, main_fighter_2) VALUES ('" + id +
                       "', '" + str(event_date) + "', '" + base_title + "', '" + title_tag_line + "', '" + subtitle +
                       "', '" + event_status + "', '" + str(last_modified) + "', '" + url_name + "', '" + main_fighter_1 +
                       "', '" + main_fighter_2 + "')")

        cnxn.commit()
        cursor.close()
        cnxn.close()

def load_fights():
    events = json.load(urllib2.urlopen("http://ufc-data-api.ufc.com/api/v3/events"))
    for i in range(80,len(events)):
        event_id = str(events[i]['id'])
        fights = json.load(urllib2.urlopen("http://ufc-data-api.ufc.com/api/v3/events/"+event_id+"/fights"))
        for i in range(len(fights)):
            print fights[i]
            id = str(fights[i]['id'])
            try:
                weight_class = fights[i]['fighter1_weight_class'] if fights[i]['fighter1_weight_class'] != None else 'null'
            except:
                global count
                weight_class = 'null'
            fighter1_id = str(fights[i]['fighter1_id'])
            fighter2_id = str(fights[i]['fighter2_id'])

            try:
                fighter1_image = fights[i]['fighter1_profile_image'] if fights[i]['fighter1_profile_image'] != None else 'null'
            except:
                fighter1_image = 'null'

            try:
                fighter2_image = fights[i]['fighter2_profile_image'] if fights[i]['fighter2_profile_image'] != None else 'null'
            except:
                fighter2_image = 'null'

            try:
                ending_round = fights[i]['ending_round_number'] if fights[i]['ending_round_number'] != None else 'null'
            except:
                ending_round = 'null'

            try:
                live_stats_url = fights[i]['fm_stats_feed_url'] if fights[i]['fm_stats_feed_url'] != None else 'null'
            except:
                live_stats_url = 'null'

            try:
                if str(fights[i]['fighter1_is_winner']) == 'true':
                    winner = fighter1_id
                else:
                    winner = fighter2_id
            except:
                winner = 'null'

            try:
                result_method = fights[i]['result']['Method'] if fights[i]['result']['Method'] != None else 'null'
                try:
                    result_method = result_method.replace("'", "''")
                except:
                    result_method = result_method
            except:
                result_method = 'null'

            cnxn = pyodbc.connect(
                'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
                ';PWD=' + password)
            cursor = cnxn.cursor()
            a = "Insert into fights(id, event_id, weight_class, live_stats_url, winner, fighter1_id, " \
                "fighter2_id, ending_round, result_method, fighter1_image, fighter2_image) VALUES ('" + id + "', '" + event_id + "', '" + weight_class + "', '" + live_stats_url + "', '" + winner +"', '" + fighter1_id + "', '" + fighter2_id + "', '" + ending_round + "', '" + result_method +"', '" + fighter1_image +"', '" + fighter2_image + "')"
            print a
            cursor.execute("Insert into fights(id, event_id, weight_class, live_stats_url, winner, fighter1_id, "
                           "fighter2_id, ending_round, result_method, fighter1_image, fighter2_image) VALUES ('" + id +
                           "', '" + event_id + "', '" + weight_class + "', '" + live_stats_url + "', '" + winner +
                           "', '" + fighter1_id + "', '" + fighter2_id + "', '" + ending_round + "', '" + result_method +
                           "', '" + fighter1_image +"', '" + fighter2_image + "')")

            cnxn.commit()
            cursor.close()
            cnxn.close()

            try:
                fighter1_reach = str(fights[i]['fighter1reach'] if fights[i]['fighter1reach'] != None else '0')
            except:
                fighter1_reach = '0'
            try:
                fighter1_weight = str(fights[i]['fighter1weight'] if fights[i]['fighter1weight'] != None else '0')
            except:
                fighter1_weight = '0'
            try:
                fighter1_height = str(fights[i]['fighter1height'] if fights[i]['fighter1height'] != None else '0')
            except:
                fighter1_height = '0'
            try:
                fighter1_avg_fight_time = fights[i]['fighter1_averagefighttime'] if fights[i]['fighter1_averagefighttime'] != None else '0'
            except:
                fighter1_avg_fight_time = 'null'
            try:
                fighter1_kd_avg = fights[i]['fighter1_kdaverage'] if fights[i]['fighter1_kdaverage'] != None else '0'
            except:
                fighter1_kd_avg = 'null'
            try:
                fighter1_slpm = fights[i]['fighter1_slpm'] if fights[i]['fighter1_slpm'] != None else '0'
            except:
                fighter1_slpm = 'null'
            try:
                fighter1_striking_accuracy = fights[i]['fighter1_strikingaccuracy'] if fights[i]['fighter1_strikingaccuracy'] != None else '0'
            except:
                fighter1_striking_accuracy = 'null'
            try:
                fighter1_sapm = fights[i]['fighter1_sapm'] if fights[i]['fighter1_sapm'] != None else '0'
            except:
                fighter1_sapm = 'null'
            try:
                fighter1_striking_defense = fights[i]['fighter1_strikingdefense'] if fights[i]['fighter1_strikingdefense'] != None else '0'
            except:
                fighter1_striking_defense = 'null'
            try:
                fighter1_takedown_avg = fights[i]['fighter1_takedownaverage'] if fights[i]['fighter1_takedownaverage'] != None else '0'
            except:
                fighter1_takedown_avg = 'null'
            try:
                fighter1_takedown_accuracy = fights[i]['fighter1_takedownaccuracy'] if fights[i]['fighter1_takedownaccuracy'] != None else '0'
            except:
                fighter1_takedown_accuracy = 'null'
            try:
                fighter1_takedown_defense = fights[i]['fighter1_takedowndefense'] if fights[i]['fighter1_takedowndefense'] != None else '0'
            except:
                fighter1_takedown_defense = 'null'
            try:
                fighter1_submission_avg = fights[i]['fighter1_submissionsaverage'] if fights[i]['fighter1_submissionsaverage'] != None else '0'
            except:
                fighter1_submission_avg = 'null'

            cnxn = pyodbc.connect(
                'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
                ';PWD=' + password)
            cursor = cnxn.cursor()
            a = "Update fighters Set reach = '"+fighter1_reach+"', weight ='"+fighter1_weight+"', height = '"+fighter1_height+"', avg_fight_time = '"+fighter1_avg_fight_time+"', kd_avg = '"+fighter1_kd_avg+"', slpm = '"+fighter1_slpm+"', striking_accuracy= '"+fighter1_striking_accuracy+"', sapm = '"+fighter1_sapm+"', striking_defense = '"+fighter1_striking_defense+"', takedown_avg = '"+fighter1_takedown_avg+"', takedown_accuracy = '"+fighter1_takedown_accuracy+"', takedown_defense = '"+fighter1_takedown_defense+"', submission_avg = '"+fighter1_submission_avg+"' where id = '"+fighter1_id+"'"
            print a
            cursor.execute("Update fighters Set reach = '"+fighter1_reach+"', weight ='"+fighter1_weight+
                           "', height = '"+fighter1_height+"', avg_fight_time = '"+fighter1_avg_fight_time+"', "
                           "kd_avg = '"+fighter1_kd_avg+"', slpm = '"+fighter1_slpm+"', "
                           "striking_accuracy= '"+fighter1_striking_accuracy+"', sapm = '"+fighter1_sapm+"', "
                           "striking_defense = '"+fighter1_striking_defense+"', takedown_avg = '"+fighter1_takedown_avg+"', "
                           "takedown_accuracy = '"+fighter1_takedown_accuracy+"', takedown_defense = '"+fighter1_takedown_defense+"', "
                           "submission_avg = '"+fighter1_submission_avg+"' where id = '"+fighter1_id+"'")
            cnxn.commit()
            cursor.close()
            cnxn.close()

            try:
                fighter2_reach = str(fights[i]['fighter2reach'] if fights[i]['fighter2reach'] != None else '0')
            except:
                fighter2_reach = '0'
            try:
                fighter2_weight = str(fights[i]['fighter2weight'] if fights[i]['fighter2weight'] != None else '0')
            except:
                fighter2_weight = '0'
            try:
                fighter2_height = str(fights[i]['fighter2height'] if fights[i]['fighter2height'] != None else '0')
            except:
                fighter2_height = '0'
            try:
                fighter2_avg_fight_time = fights[i]['fighter2_averagefighttime'] if fights[i]['fighter2_averagefighttime'] != None else '0'
            except:
                fighter2_avg_fight_time = 'null'
            try:
                fighter2_kd_avg = fights[i]['fighter2_kdaverage'] if fights[i]['fighter2_kdaverage'] != None else '0'
            except:
                fighter2_kd_avg = 'null'
            try:
                fighter2_slpm = fights[i]['fighter2_slpm'] if fights[i]['fighter2_slpm'] != None else '0'
            except:
                fighter2_slpm = 'null'
            try:
                fighter2_striking_accuracy = fights[i]['fighter2_strikingaccuracy'] if fights[i]['fighter2_strikingaccuracy'] != None else '0'
            except:
                fighter2_striking_accuracy = 'null'
            try:
                fighter2_sapm = fights[i]['fighter2_sapm'] if fights[i]['fighter2_sapm'] != None else '0'
            except:
                fighter2_sapm = 'null'
            try:
                fighter2_striking_defense = fights[i]['fighter2_strikingdefense'] if fights[i]['fighter2_strikingdefense'] != None else '0'
            except:
                fighter2_striking_defense = 'null'
            try:
                fighter2_takedown_avg = fights[i]['fighter2_takedownaverage'] if fights[i]['fighter2_takedownaverage'] != None else '0'
            except:
                fighter2_takedown_avg = 'null'
            try:
                fighter2_takedown_accuracy = fights[i]['fighter2_takedownaccuracy'] if fights[i]['fighter2_takedownaccuracy'] != None else '0'
            except:
                fighter2_takedown_accuracy = 'null'
            try:
                fighter2_takedown_defense = fights[i]['fighter2_takedowndefense'] if fights[i]['fighter2_takedowndefense'] != None else '0'
            except:
                fighter2_takedown_defense = 'null'
            try:
                fighter2_submission_avg = fights[i]['fighter2_submissionsaverage'] if fights[i]['fighter2_averagefighttime'] != None else '0'
            except:
                fighter2_submission_avg = 'null'

            cnxn = pyodbc.connect(
                'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
                ';PWD=' + password)
            cursor = cnxn.cursor()
            cursor.execute("Update fighters Set reach = '"+fighter2_reach+"', weight ='"+fighter2_weight+
                           "', height = '"+fighter2_height+"', avg_fight_time = '"+fighter2_avg_fight_time+"', "
                           "kd_avg = '"+fighter2_kd_avg+"', slpm = '"+fighter2_slpm+"', "
                           "striking_accuracy= '"+fighter2_striking_accuracy+"', sapm = '"+fighter2_sapm+"', "
                           "striking_defense = '"+fighter2_striking_defense+"', takedown_avg = '"+fighter2_takedown_avg+"', "
                           "takedown_accuracy = '"+fighter2_takedown_accuracy+"', takedown_defense = '"+fighter2_takedown_defense+"', "
                           "submission_avg = '"+fighter2_submission_avg+"' where id = '"+fighter2_id+"'")
            cnxn.commit()
            cursor.close()
            cnxn.close()

load_fights()
# def load_live_fight_data(fight_id):
#     live_data = json.load(urllib2.urlopen("http://liveapi.fightmetric.com/V2/647/4636/Stats.json"))
#
#     max_rounds = live_data['FMLiveFeed']['MaxRounds']
#
#     round_1 = live_data['FMLiveFeed']['RoundStats']['Round 1']
#
#     print max_rounds
#
# load_live_fight_data(1)