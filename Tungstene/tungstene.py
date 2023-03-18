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
	viewer = []
	r = requests.get('https://tmi.twitch.tv/group/user/'+channel+'/chatters') #Get users in chat
	data = r.json()['chatters']
	for key in data.keys():
		viewer += r.json()['chatters'][key]
	return viewer
	
def is_number(nbr):
	if type(nbr) == bool:
		return False
	try:
		float(nbr)
		return True
	except ValueError:
		return False

def verification(database,resp,channel):
	if(channel in database.keys()): #Verify if streamer is in the db
		for viewer in resp: #For viewers in the chat scan
			if(viewer not in database[channel]): #If viewer not in db
				database[channel].append(viewer) #add him
	else:
		database[channel] = resp #Just write the chat users for the first time

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
		nodes.append({"id":streamer,"type":"streamer","value":5}) #Create node for streamer
		for viewer in data[streamer]: #For every viewer of every streamers
			if viewer not in logins: #If viewer not registered -> create node too
				logins.append(viewer) #Add viewer to list
				nodes.append({"id":viewer,"type":"viewer","value":5}) #Create node
			links.append({"source":viewer,"target":streamer}) #Create link

	write("./data/"+config['output']['nodes'],nodes) #Write nodes.json file
	write("./data/"+config['output']['links'],links) #Write links.json file
	print(f'[LOGS] Output files written. Total users registered : {len(logins)}')

def game_scan():
	display_init()
	print("[LOGS] No configuration set, treating this as Game ID Research")
	games = twitch.search_categories(input("[INPUT] Category Name : "))

	for game in games["data"]:
		print("[LOGS] " + game["name"] + " | id : " + game["id"])
	print(f"[EXIT] Program ended due to end of process")

def game_scan_config(name_game_scan):
	games = twitch.search_categories(name_game_scan)["data"]
	print(f"[LOGS] Found {len(games)} games with that name :")
	for number_game in range(len(games)) :
		print(f"[LOGS] - {number_game+1} : " + games[number_game]["name"] + " -")
	choice_game = int(input("[INPUT] Input ID of chosen game : "))
	return games[choice_game-1]["id"]

def type_scan_config() :
	input_type = True
	list_type = ("Game","Language","Streamer","Global","Game-Language")
	while input_type is not False :
		print("[CONFIG] Types of scans possible :")
		print(" - (Game) Scan the top of a specific game ")
		print(" - (Language) Scan the top of a specific language ")
		print(" - (Streamer) Scan the top of specific streams ")
		print(" - (Global) Scan the top of all of Twitch ")
		print(" - (Game-Language) Hybrid of the two ")
		input_type = input("[INPUT] Type of scan asked : ")
		if input_type in list_type :
			return input_type
		
def create_config(config):
	display_init()
	type_scan = type_scan_config()
	config = {"requests":{"delay":'none',"start":'none',"end":'none'},"output":{"nodes":'',"links":''},"scan":{"game_id":False,"language":False,"top_length":False,"streamers":False,"global_scan":False},"creds":{"id_twitch":config["creds"]["id_twitch"],"secret_twitch":config["creds"]["secret_twitch"]},"cmd_config":False,"chat_scan":{"enable":False,"words_lookup":[]}}

	print("[CONFIG] Request Setup")
	while is_number(config["requests"]["delay"]) is not True:
		config["requests"]["delay"] = input("[INPUT] Delay between requests (in seconds) : ")
	while is_number(config["requests"]["start"])is not True:
		config["requests"]["start"] = input("[INPUT] Time to start (UnixTimeStamp) : ")
	while is_number(config["requests"]["end"]) is not True:
		config["requests"]["end"] = input("[INPUT] Time to end (UnixTimeStamp) : ")
		
	config["requests"]["delay"] = int(config["requests"]["delay"])
	config["requests"]["start"] = float(config["requests"]["start"])
	config["requests"]["end"] = float(config["requests"]["end"])

	print("[CONFIG] Output Setup")
	while config["output"]["nodes"] == "":
		config["output"]["nodes"] = input("[INPUT] Name of the nodes file (existing .json file) : ")
	while config["output"]["links"] == "":
		config["output"]["links"] = input("[INPUT] Name of the links file (existing .json file) : ")

	print("[CONFIG] Scan Setup")
	if type_scan == "Game" or type_scan == "Game-Language" :
		Game_id_input = input("[INPUT] Name/ID of the game to scan : ")
		if is_number(Game_id_input) is True :
			config["scan"]["game_id"] = Game_id_input
		else :
			config["scan"]["game_id"] = game_scan_config(Game_id_input)
	if type_scan == "Language" or type_scan == "Game-Language" :
		while config["scan"]["language"] == False :
			language_input = input("[INPUT] Language of the Streams (format : ##) : ")
			if len(language_input) == 2 and (is_number(language_input) is not True) :
				config["scan"]["language"] = language_input
	if type_scan != "Streamer" :
		while is_number(config["scan"]["top_length"]) is not True or (int(config["scan"]["top_length"]) <= 100 and int(config["scan"]["top_length"]) >= 1) is False:
			config["scan"]["top_length"] = input("[INPUT] Number of channel scanned (1-100) : ")
		config["scan"]["top_length"] = int(config["scan"]["top_length"])
	if type_scan == "Streamer" :
		while config["scan"]["streamers"] == False :
			list_streamers_input = []
			while len(list_streamers_input) == 0 or list_streamers_input[-1] != "" :
				list_streamers_input.append(input("[INPUT] Link of streamer to scan:  "))
			list_streamers_input.pop(-1)
			config["scan"]["streamers"] = list_streamers_input
	if type_scan == "Global" :
		config["scan"]["global_scan"] = True

	with open('config.yml', 'w') as config_file:
		data = json.loads(str(config).replace("'",'"').replace("False","false").replace("True","true"))
		yaml.dump(data, config_file, allow_unicode=True)

	print("[CONFIG] Setup Ended")

def chat_stat(streamer_name,chatters):
	database = read('./data/viewtime.json')
	if streamer_name not in database.keys() :
		chatter_time = {}
		for chatter in chatters :
			chatter_time[chatter] = 0
		database[streamer_name] = chatter_time
	else :
		for chatter in chatters :
			if chatter not in database[streamer_name].keys() :
				database[streamer_name][chatter] = 0
			else :
				database[streamer_name][chatter] += config["requests"]["delay"]
	write('./data/viewtime.json',database)

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

	database = read('./data/global_map.json') #Set global_map.json as dump file for scan

	display_temp = config['requests']['start']-time.time()
	display_temp_global = time.gmtime(config['requests']['start'])
	print(f'[WARMUP] Starting in {display_temp} seconds (or {display_temp_global[3]+1}:{display_temp_global[4]}:{display_temp_global[5]} {display_temp_global[2]}/{display_temp_global[1]}/{display_temp_global[0]} UTC+1)')
	time.sleep(config['requests']['start']-time.time()) #Awaiting start time

	display_temp = config['requests']['end']-time.time()
	display_temp_global = time.gmtime(config['requests']['end'])
	print(f'[LOGS] Starting Protocols --- Ending in {display_temp} seconds (or {display_temp_global[3]+1}:{display_temp_global[4]}:{display_temp_global[5]} {display_temp_global[2]}/{display_temp_global[1]}/{display_temp_global[0]} UTC+1)')

	while(time.time() < config['requests']['end']):
		compensate = time.time()
		for channel in streamers_list: #For every streamer login in our list
			try:
				resp = api_requests(channel)
				database = verification(database,resp,channel)
				chat_stat(channel,resp)
			except ValueError:
				True
			write('./data/global_map.json',database)
			print(f'[{datetime.now().strftime("%H:%M:%S")}][LOGS] Everything went right. Waiting for next scan')

		try:
			time.sleep(config['requests']['delay']-(time.time()-compensate)) #Await delay until next scan
		except ValueError:
			print(f'[{datetime.now().strftime("%H:%M:%S")}][ERROR] Scan went further than expected : going forward anyway.')

	print(f'[{datetime.now().strftime("%H:%M:%S")}][LOGS] Query ended due to time limit')

	file_constructor('./data/global_map.json') #Construct end file
	print(f'[{datetime.now().strftime("%H:%M:%S")}][EXIT] Program ended due to end of process') #End of process

def main(config):
	if(config['cmd_config'] == False):
		if input("[INPUT] Previous Configuration loaded, set new config ? (y/n) : ") == 'y' :
			config = create_config(config)
	elif(config['cmd_config'] == True):
		config = create_config(config)
	if(config['scan']['streamers'] != False): #If streamer list is define in config
		streamers_list = config['scan']['streamers']
		scan(streamers_list)

	elif(config['scan']['game_id'] != False): #If game_id is define in config
		if(config['scan']['language'] != False):
			streamers_list = [channel['user_login'] for channel in twitch.get_streams(game_id = config['scan']['game_id'], first = config['scan']['top_length'], language = config['scan']['language'])['data']] #Add language filter
		else:
			streamers_list = [channel['user_login'] for channel in twitch.get_streams(game_id = config['scan']['game_id'], first = config['scan']['top_length'])['data']] #No language filter
		scan(streamers_list) #Launch Game scan (with or without language filter)

	elif(config['scan']['language'] != False): #If language is define in config
		streamers_list = [channel['user_login'] for channel in twitch.get_streams(first = config['scan']['top_length'], language = config['scan']['language'])['data']]
		scan(streamers_list) #Launch Language scan

	elif(config['scan']['global_scan'] == True): #If language is not define
		streamers_list = [channel['user_login'] for channel in twitch.get_streams(first = config['scan']['top_length'])['data']]
		scan(streamers_list) #Launch Global scan

	else:
		game_scan() #Launch GameID scan
    
if __name__ == '__main__':
	main(config)
