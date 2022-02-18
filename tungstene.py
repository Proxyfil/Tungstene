#Imports
import requests
import time
import yaml
import json
from twitchAPI.twitch import Twitch
import os
from datetime import datetime

#Variables Declarements
config_file = 'config.yml'


config_yml = open(config_file,'r',encoding='utf-8')
config = yaml.load(config_yml, Loader=yaml.loader.SafeLoader)

secret_client = config['creds']['secret_twitch']
id_client = config['creds']['id_twitch']

twitch = Twitch(id_client, secret_client)
twitch.authenticate_app([])

#Functions Declarement
def api_requests(channel):
    r = requests.get('https://tmi.twitch.tv/group/user/'+channel+'/chatters') #Get users in chat
    return r.json()['chatters']['viewers']

def verification(database,resp,channel):
    if(channel in database.keys()): #Verify if streamer is in the db
            for viewer in resp: #For viewers in the chat scan
                if(viewer not in database[channel]): #If viewer not in db
                    database[channel].append(viewer) #add him
    else:
        database[channel] = resp #Just right the chat users for the first time

    return database

def read(file):
    data = open(file,'r',encoding='utf-8')
    content = ''
    for char in data:
        content += char
    return json.loads(content)

def write(file,data):
    database_file = open(file,'w',encoding='utf-8') #Open dump file
    database_file.write(str(data).replace("'",'"'))
    #json.dump(data, database_file, indent = 4) #Write in file
    database_file.close() #Close file

def display_init():
    print(" ______                                 __                            \n/\__  _\                               /\ \__                         \n\/_/\ \/ __  __    ___      __     ____\ \ ,_\    __    ___      __   \n   \ \ \/\ \/\ \ /' _ `\  /'_ `\  /',__\\ \ \/  /'__`\/' _ `\  /'__`\ \n    \ \ \ \ \_\ \/\ \/\ \/\ \L\ \/\__, `\\ \ \_/\  __//\ \/\ \/\  __/ \n     \ \_\ \____/\ \_\ \_\ \____ \/\____/ \ \__\ \____\ \_\ \_\ \____\ \n      \/_/\/___/  \/_/\/_/\/___L\ \/___/   \/__/\/____/\/_/\/_/\/____/\n                            /\____/                                   \n                            \_/__/                                    \n")

def file_constructor(file):
    logins = []
    nodes = []
    links = []
    data = read(file) #Get data from dump file

    for streamer in data.keys():
        logins.append(streamer) #Add streamer to list
        nodes.append({"i":streamer,"t":"s"}) #Create node for streamer
        for viewer in data[streamer]: #For every viewer of every streamers
            if viewer not in logins: #If viewer not registered -> create node too
                logins.append(viewer) #Add viewer to list
                nodes.append({"i":viewer,"t":"v"}) #Create node
            links.append({"s":viewer,"t":streamer}) #Create link

    write(config['output']['nodes'],nodes) #Write nodes.json file
    write(config['output']['links'],links) #Write links.json file
    print(f'[LOGS] Output files written. Total users registered : {len(logins)}')


def scan(streamers_list):
    display_init() #Logo
    print(f'[WARMUP] Starting every protocols...')
    print(f'[WARMUP] Config file as {config_file}')

    if(config['requests']['start']-time.time() < 0): #Start to actual time to avoid bugs
        print('[ERROR] Start timestamp is in the past. Setting start time in 1 second')
        config['requests']['start'] = time.time()+1

    if(config['requests']['start']-time.time() > config['requests']['end']-time.time()): #Start after End -> Error
        print('[ERROR] Start timestamp is after End Timestamp... You can\'t do this :/')
        exit()

    database = read('global_map.json') #Set global_map.json as dump file for scan

    display_temp = config['requests']['start']-time.time()
    display_temp_global = time.gmtime(config['requests']['start'])
    print(f'[WARMUP] Starting in {display_temp} seconds (or {display_temp_global[3]+1}:{display_temp_global[4]}:{display_temp_global[5]} {display_temp_global[2]}/{display_temp_global[1]}/{display_temp_global[0]} UTC+1)')
    time.sleep(config['requests']['start']-time.time()) #Awaiting start time

    display_temp = config['requests']['end']-time.time()
    display_temp_global = time.gmtime(config['requests']['end'])
    print(f'[LOGS] Starting Protocols --- Ending in {display_temp} seconds (or {display_temp_global[3]+1}:{display_temp_global[4]}:{display_temp_global[5]} {display_temp_global[2]}/{display_temp_global[1]}/{display_temp_global[0]} UTC+1)')

    while(time.time() < config['requests']['end']):
        try:
            for channel in streamers_list: #For every streamer login in our list
                resp = api_requests(channel)
                database = verification(database,resp,channel)
            write('global_map.json',database)
            print(f'[{datetime.now().strftime("%H:%M:%S")}][LOGS] Everything went right. Waiting for next scan')
        except ValueError:
            print(f'[{datetime.now().strftime("%H:%M:%S")}][ERROR] An error occured, waiting for next scan : {ValueError}')

        time.sleep(config['requests']['delay']) #Await delay until next scan

    print(f'[{datetime.now().strftime("%H:%M:%S")}][LOGS] Query ended due to time limit')

    file_constructor('global_map.json') #Construct end file
    print(f'[{datetime.now().strftime("%H:%M:%S")}][EXIT] Program ended due to end of process') #End of process

    
if __name__ == '__main__':
    if(config['scan']['streamers'] != False): #If streamer list is define in config
        streamers_list = config['scan']['streamers']
        scan(streamers_list)

    elif(config['scan']['game_id'] != ''): #If game_id is define in config
        if(config['scan']['language'] != ''):
            streamers_list = [channel['user_login'] for channel in twitch.get_streams(game_id = config['scan']['game_id'], first = config['scan']['top_lenght'], language = config['scan']['language'])['data']] #Add language filter
        else:
            streamers_list = [channel['user_login'] for channel in twitch.get_streams(game_id = config['scan']['game_id'], first = config['scan']['top_lenght'])['data']] #No language filter
        scan(streamers_list) #Launch Game scan (with or without language filter)

    elif(config['scan']['language'] != ''): #If language is define in config
        streamers_list = [channel['user_login'] for channel in twitch.get_streams(first = config['scan']['top_lenght'], language = config['scan']['language'])['data']]
        scan(streamers_list) #Launch Language scan

    elif(config['scan']['language'] == ''): #If language is not define
        streamers_list = [channel['user_login'] for channel in twitch.get_streams(first = config['scan']['top_lenght'])['data']]
        scan(streamers_list) #Launch Global scan

    else:
        game_scan() #Launch GameID scan