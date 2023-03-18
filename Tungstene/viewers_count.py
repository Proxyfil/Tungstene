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


def read(file):
	data = open(file,'r',encoding='utf-8')
	content = ''
	for char in data:
		content += char
	return json.loads(content)

def write(file,data):
	database_file = open(file,'w',encoding='utf-8') #Open dump file
	#database_file.write(str(data).replace("'",'"'))
	json.dump(data, database_file, indent = 4) #Write in file
	database_file.close() #Close file

display_temp = config['requests']['start']-time.time()
display_temp_global = time.gmtime(config['requests']['start'])
print(f'[WARMUP] Starting in {display_temp} seconds (or {display_temp_global[3]+1}:{display_temp_global[4]}:{display_temp_global[5]} {display_temp_global[2]}/{display_temp_global[1]}/{display_temp_global[0]} UTC+1)')
time.sleep(config['requests']['start']-time.time()) #Awaiting start time

display_temp = config['requests']['end']-time.time()
display_temp_global = time.gmtime(config['requests']['end'])
print(f'[LOGS] Starting Protocols --- Ending in {display_temp} seconds (or {display_temp_global[3]+1}:{display_temp_global[4]}:{display_temp_global[5]} {display_temp_global[2]}/{display_temp_global[1]}/{display_temp_global[0]} UTC+1)')
	

while(time.time() < config['requests']['end']):
	viewers = read('./data/viewer_graph.json')
	compensate = time.time()
	for channel in config['scan']['streamers']: #For every streamer login in our list
		try:
			streams = twitch.get_streams(user_login=channel,first=1)["data"]
			if(channel not in list(viewers.keys())):
				viewers[channel] = []

			if(len(streams) != 0):
				viewers[channel].append(streams[0]['viewer_count'])
			else:
				viewers[channel].append(0)
		except ValueError:
			True
	
	write('./data/viewer_graph.json',viewers)
	print(f'[{datetime.now().strftime("%H:%M:%S")}][LOGS] Everything went right. Waiting for next scan')
	time.sleep(900-(time.time()-compensate)) #Await delay until next scan

print(f'[{datetime.now().strftime("%H:%M:%S")}][LOGS] Query ended due to time limit')