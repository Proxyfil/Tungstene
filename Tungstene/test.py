import requests
import time
import yaml
import json
from twitchAPI.twitch import Twitch
import os
from datetime import datetime

config_yml = open('./config.yml','r',encoding='utf-8')
config = yaml.load(config_yml, Loader=yaml.loader.SafeLoader)

secret_client = config['creds']['secret_twitch']
id_client = config['creds']['id_twitch']

twitch = Twitch(id_client, secret_client)
twitch.authenticate_app([])

streamers = config["scan"]["streamers"]

for streamer in streamers:
	if(twitch.get_users(logins = streamer)["data"] == []):
		print(f'Error with {streamer}')



