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
    print len(events)
    for i in range(len()):
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


def load_live_fight_data():
    count = 0
    events = json.load(urllib2.urlopen("http://ufc-data-api.ufc.com/api/v3/events"))
    print len(events)
    for j in range(8,88):
        print j
        event_id = str(events[j]['id'])
        print event_id
        fights = json.load(urllib2.urlopen("http://ufc-data-api.ufc.com/api/v3/events/" + event_id + "/fights"))
        for i in range(len(fights)):
            fight_id = str(fights[i]['id'])
            fighter1_id = str(fights[i]['fighter1_id'])
            fighter1_name = fights[i]['fighter1_first_name']+" "+ fights[i]['fighter1_last_name']
            print fighter1_name
            fighter2_id = str(fights[i]['fighter2_id'])
            fighter2_name = fights[i]['fighter2_first_name']+" "+ fights[i]['fighter2_last_name']
            print fighter2_name
            live_stats_url = fights[i]['fm_stats_feed_url'] if fights[i]['fm_stats_feed_url'] != None else 'null'
            try:
                live_data = json.load(urllib2.urlopen(live_stats_url))
            except:
                live_data = '0'

            if live_data != '0':
                try:
                    max_rounds = live_data['FMLiveFeed']['CurrentRound']
                    if live_stats_url == 'http://liveapi.fightmetric.com/V2/745/5632/Stats.json':
                        max_rounds += 1
                except:
                    continue

                if fighter1_name != live_data['FMLiveFeed']['Fighters']['Red']['Name'] and fighter2_name != live_data['FMLiveFeed']['Fighters']['Blue']['Name']:
                    print False
                    temp = fighter1_id
                    fighter1_id = fighter2_id
                    fighter2_id = temp
                    del temp
                    count += 1

                for i in range(1,int(max_rounds)):
                    if i == 2 and live_stats_url == 'http://liveapi.fightmetric.com/V2/745/5632/Stats.json':
                        continue
                    round_num = i
                    print "Round is %s" % round_num
                    fighter1_knock_down_landed = live_data['FMLiveFeed']['RoundStats']['Round%s'%i]['Red']['Strikes']['Knock Down']['Landed']
                    fighter1_significant_strikes= live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Significant Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Significant Strikes']['Attempts']
                    fighter1_total_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Total Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Total Strikes']['Attempts']
                    fighter1_punches = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Punches']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Punches']['Attempts']
                    fighter1_kicks = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Kicks']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Kicks']['Attempts']
                    fighter1_distance_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Strikes']['Attempts']
                    fighter1_clinch_significant_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Clinch Significant Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Clinch Significant Strikes']['Attempts']
                    fighter1_ground_significant_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Ground Significant Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Ground Significant Strikes']['Attempts']
                    fighter1_clinch_total_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Clinch Total Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Clinch Total Strikes']['Attempts']
                    fighter1_ground_total_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Ground Total Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Ground Total Strikes']['Attempts']
                    fighter1_head_total_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Head Total Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Head Total Strikes']['Attempts']
                    fighter1_body_total_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Body Total Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Body Total Strikes']['Attempts']
                    fighter1_legs_total_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Legs Total Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Legs Total Strikes']['Attempts']
                    fighter1_head_significant_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Head Significant Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Head Significant Strikes']['Attempts']
                    fighter1_body_significant_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Body Significant Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Body Significant Strikes']['Attempts']
                    fighter1_legs_significant_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Legs Significant Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Legs Significant Strikes']['Attempts']
                    fighter1_distance_head_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Head Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Head Strikes']['Attempts']
                    fighter1_distance_body_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Body Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Body Strikes']['Attempts']
                    fighter1_distance_leg_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Leg Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Leg Strikes']['Attempts']
                    fighter1_clinch_head_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Clinch Head Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Clinch Head Strikes']['Attempts']
                    fighter1_clinch_body_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Clinch Body Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Clinch Body Strikes']['Attempts']
                    fighter1_clinch_leg_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Clinch Leg Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Clinch Leg Strikes']['Attempts']
                    fighter1_ground_head_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Ground Head Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Ground Head Strikes']['Attempts']
                    fighter1_ground_body_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Ground Body Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Ground Body Strikes']['Attempts']
                    fighter1_ground_leg_strikes = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Ground Leg Strikes']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Ground Leg Strikes']['Attempts']
                    fighter1_distance_head_kicks = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Head Kicks']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Head Kicks']['Attempts']
                    fighter1_distance_body_kicks = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Body Kicks']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Head Kicks']['Attempts']
                    fighter1_distance_leg_kicks = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Leg Kicks']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Leg Kicks']['Attempts']
                    try:
                        fighter1_distance_head_punches = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Head Punhces']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Head Punches']['Attempts']
                    except:
                        fighter1_distance_head_punches = '0:0'
                    try:
                        fighter1_distance_body_punches = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Body Punhces']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Body Punches']['Attempts']
                    except:
                        fighter1_distance_body_punches = '0:0'
                    try:
                        fighter1_distance_body_punches = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Body Punhces']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Distance Body Punches']['Attempts']
                    except:
                        fighter1_distance_body_punches = '0:0'
                    try:
                        fighter1_clinch_significant_kicks = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Clinch Significant Kicks']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Clinch Significant Kicks']['Attempts']
                    except:
                        fighter1_clinch_significant_kicks = '0:0'
                    fighter1_clinch_significant_punches = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Clinch Significant Punches']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Clinch Significant Punches']['Attempts']
                    fighter1_ground_significant_kicks = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Ground Significant Kicks']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Ground Significant Kicks']['Attempts']
                    fighter1_ground_significant_punches = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Ground Significant Punches']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Strikes']['Ground Significant Punches']['Attempts']
                    fighter1_takedowns = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Grappling']['Takedowns']['Landed'] + ":" + live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Grappling']['Takedowns']['Attempts']
                    fighter1_submissions = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Grappling']['Submissions']['Attempts']
                    fighter1_reversals_landed = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Grappling']['Reversals']['Landed']
                    fighter1_standups_landed = live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Red']['Grappling']['Standups']['Landed']

                    fighter2_knock_down_landed = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Knock Down']['Landed']
                    fighter2_significant_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Significant Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Significant Strikes'][
                        'Attempts']
                    fighter2_total_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Total Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Total Strikes']['Attempts']
                    fighter2_punches = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Punches']['Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Punches']['Attempts']
                    fighter2_kicks = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Kicks']['Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Kicks']['Attempts']
                    fighter2_distance_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Distance Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Distance Strikes'][
                        'Attempts']
                    fighter2_clinch_significant_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                        'Clinch Significant Strikes']['Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                        'Clinch Significant Strikes']['Attempts']
                    fighter2_ground_significant_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                        'Ground Significant Strikes']['Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                        'Ground Significant Strikes']['Attempts']
                    fighter2_clinch_total_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Clinch Total Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Clinch Total Strikes'][
                        'Attempts']
                    fighter2_ground_total_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Ground Total Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Ground Total Strikes'][
                        'Attempts']
                    fighter2_head_total_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Head Total Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Head Total Strikes'][
                        'Attempts']
                    fighter2_body_total_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Body Total Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Body Total Strikes'][
                        'Attempts']
                    fighter2_legs_total_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Legs Total Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Legs Total Strikes'][
                        'Attempts']
                    fighter2_head_significant_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Head Significant Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Head Significant Strikes'][
                        'Attempts']
                    fighter2_body_significant_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Body Significant Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Body Significant Strikes'][
                        'Attempts']
                    fighter2_legs_significant_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Legs Significant Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Legs Significant Strikes'][
                        'Attempts']
                    fighter2_distance_head_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Distance Head Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Distance Head Strikes'][
                        'Attempts']
                    fighter2_distance_body_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Distance Body Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Distance Body Strikes'][
                        'Attempts']
                    fighter2_distance_leg_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Distance Leg Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Distance Leg Strikes'][
                        'Attempts']
                    fighter2_clinch_head_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Clinch Head Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Clinch Head Strikes'][
                        'Attempts']
                    fighter2_clinch_body_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Clinch Body Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Clinch Body Strikes'][
                        'Attempts']
                    fighter2_clinch_leg_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Clinch Leg Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Clinch Leg Strikes'][
                        'Attempts']
                    fighter2_ground_head_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Ground Head Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Ground Head Strikes'][
                        'Attempts']
                    fighter2_ground_body_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Ground Body Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Ground Body Strikes'][
                        'Attempts']
                    fighter2_ground_leg_strikes = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Ground Leg Strikes'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Ground Leg Strikes'][
                        'Attempts']
                    fighter2_distance_head_kicks = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Distance Head Kicks'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Distance Head Kicks'][
                        'Attempts']
                    fighter2_distance_body_kicks = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Distance Body Kicks'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Distance Head Kicks'][
                        'Attempts']
                    fighter2_distance_leg_kicks = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Distance Leg Kicks'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Distance Leg Kicks'][
                        'Attempts']
                    try:
                        fighter2_distance_head_punches = \
                        live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                            'Distance Head Punhces']['Landed'] + ":" + \
                        live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                            'Distance Head Punches']['Attempts']
                    except:
                        fighter2_distance_head_punches = '0:0'
                    try:
                        fighter2_distance_body_punches = \
                        live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                            'Distance Body Punhces']['Landed'] + ":" + \
                        live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                            'Distance Body Punches']['Attempts']
                    except:
                        fighter2_distance_body_punches = '0:0'
                    try:
                        fighter2_distance_body_punches = \
                        live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                            'Distance Body Punhces']['Landed'] + ":" + \
                        live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                            'Distance Body Punches']['Attempts']
                    except:
                        fighter2_distance_body_punches = '0:0'
                    try:
                        fighter2_clinch_significant_kicks = \
                        live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                            'Clinch Significant Kicks']['Landed'] + ":" + \
                        live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                            'Clinch Significant Kicks']['Attempts']
                    except:
                        fighter2_clinch_significant_kicks = '0:0'
                    fighter2_clinch_significant_punches = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                        'Clinch Significant Punches']['Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                        'Clinch Significant Punches']['Attempts']
                    fighter2_ground_significant_kicks = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Ground Significant Kicks'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes']['Ground Significant Kicks'][
                        'Attempts']
                    fighter2_ground_significant_punches = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                        'Ground Significant Punches']['Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Strikes'][
                        'Ground Significant Punches']['Attempts']
                    fighter2_takedowns = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Grappling']['Takedowns'][
                        'Landed'] + ":" + \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Grappling']['Takedowns']['Attempts']
                    fighter2_submissions = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Grappling']['Submissions']['Attempts']
                    fighter2_reversals_landed = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Grappling']['Reversals']['Landed']
                    fighter2_standups_landed = \
                    live_data['FMLiveFeed']['RoundStats']['Round%s' % i]['Blue']['Grappling']['Standups']['Landed']

                    try:
                        cnxn = pyodbc.connect(
                            'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
                            ';PWD=' + password)
                        cursor = cnxn.cursor()
                        cursor.execute(
                            "Insert into live_fight_data(fight_id, round, fighter_id, knock_down_landed, significant_strikes, "
                            "total_strikes, punches, kicks, distance_strikes, clinch_significant_strikes, "
                            "ground_significant_strikes, clinch_total_strikes, ground_total_strikes, head_significant_strikes, "
                            "body_significant_strikes, legs_significant_strikes, head_total_strikes, body_total_strikes, "
                            "legs_total_strikes, distance_head_strikes, distance_body_strikes, distance_leg_strikes,"
                            "clinch_head_strikes, clinch_body_strikes, clinch_leg_strikes, ground_head_strikes, "
                            "ground_body_strikes, ground_leg_strikes, distance_head_kicks, distance_body_kicks, distance_leg_kicks, "
                            "distance_head_punches, distance_body_punches, clinch_significant_kicks, clinch_significant_punches, "
                            "ground_significant_kicks, ground_significant_punches, takedowns, submissions, reversals_landed, "
                            "standups_landed) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', "
                            "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', "
                            "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (fight_id, round_num,
                            fighter1_id, fighter1_knock_down_landed, fighter1_significant_strikes, fighter1_total_strikes, fighter1_punches,
                            fighter1_kicks, fighter1_distance_strikes, fighter1_clinch_significant_strikes, fighter1_ground_significant_strikes,
                            fighter1_clinch_total_strikes, fighter1_ground_total_strikes, fighter1_head_significant_strikes,
                            fighter1_body_significant_strikes, fighter1_legs_significant_strikes, fighter1_head_total_strikes, fighter1_body_total_strikes,
                            fighter1_legs_total_strikes, fighter1_distance_head_strikes, fighter1_distance_body_strikes, fighter1_distance_leg_strikes,
                            fighter1_clinch_head_strikes, fighter1_clinch_body_strikes, fighter1_clinch_leg_strikes, fighter1_ground_head_strikes,
                            fighter1_ground_body_strikes, fighter1_ground_leg_strikes, fighter1_distance_head_kicks, fighter1_distance_body_kicks,
                            fighter1_distance_leg_kicks, fighter1_distance_head_punches, fighter1_distance_body_punches, fighter1_clinch_significant_kicks,
                            fighter1_clinch_significant_punches, fighter1_ground_significant_kicks, fighter1_ground_significant_punches, fighter1_takedowns,
                            fighter1_submissions, fighter1_reversals_landed, fighter1_standups_landed))
                        cursor.execute(
                            "Insert into live_fight_data(fight_id, round, fighter_id, knock_down_landed, significant_strikes, "
                            "total_strikes, punches, kicks, distance_strikes, clinch_significant_strikes, "
                            "ground_significant_strikes, clinch_total_strikes, ground_total_strikes, head_significant_strikes, "
                            "body_significant_strikes, legs_significant_strikes, head_total_strikes, body_total_strikes, "
                            "legs_total_strikes, distance_head_strikes, distance_body_strikes, distance_leg_strikes,"
                            "clinch_head_strikes, clinch_body_strikes, clinch_leg_strikes, ground_head_strikes, "
                            "ground_body_strikes, ground_leg_strikes, distance_head_kicks, distance_body_kicks, distance_leg_kicks, "
                            "distance_head_punches, distance_body_punches, clinch_significant_kicks, clinch_significant_punches, "
                            "ground_significant_kicks, ground_significant_punches, takedowns, submissions, reversals_landed, "
                            "standups_landed) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', "
                            "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', "
                            "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (fight_id, round_num,
                            fighter2_id, fighter2_knock_down_landed, fighter2_significant_strikes, fighter2_total_strikes, fighter2_punches,
                            fighter2_kicks, fighter2_distance_strikes, fighter2_clinch_significant_strikes, fighter2_ground_significant_strikes,
                            fighter2_clinch_total_strikes, fighter2_ground_total_strikes, fighter2_head_significant_strikes,
                            fighter2_body_significant_strikes, fighter2_legs_significant_strikes, fighter2_head_total_strikes, fighter2_body_total_strikes,
                            fighter2_legs_total_strikes, fighter2_distance_head_strikes, fighter2_distance_body_strikes, fighter2_distance_leg_strikes,
                            fighter2_clinch_head_strikes, fighter2_clinch_body_strikes, fighter2_clinch_leg_strikes, fighter2_ground_head_strikes,
                            fighter2_ground_body_strikes, fighter2_ground_leg_strikes, fighter2_distance_head_kicks, fighter2_distance_body_kicks,
                            fighter2_distance_leg_kicks, fighter2_distance_head_punches, fighter2_distance_body_punches, fighter2_clinch_significant_kicks,
                            fighter2_clinch_significant_punches, fighter2_ground_significant_kicks, fighter2_ground_significant_punches, fighter2_takedowns,
                            fighter2_submissions, fighter2_reversals_landed, fighter2_standups_landed))
                        cnxn.commit()
                        cursor.close()
                        cnxn.close()
                    except:
                        continue


if __name__ == '__main__':
    load_fighters()
    load_events()
    load_fights()
    load_live_fight_data()