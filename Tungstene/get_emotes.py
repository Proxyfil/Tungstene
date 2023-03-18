import yaml
import json
from twitchAPI.twitch import Twitch

config_file = 'config.yml'

config_yml = open(config_file,'r',encoding='utf-8')
config = yaml.load(config_yml, Loader=yaml.loader.SafeLoader)

secret_client = config['creds']['secret_twitch']
id_client = config['creds']['id_twitch']

twitch = Twitch(id_client, secret_client)
twitch.authenticate_app([])

users_id = []
emotes = []

for i in twitch.get_users(logins=config["scan"]["streamers"])["data"]:
    users_id.append(i["id"])

for i in users_id:
    emote_set = twitch.get_channel_emotes(broadcaster_id=i)["data"]
    broadcaster = twitch.get_users(user_ids=[i])["data"][0]["login"]

    for e in emote_set:
        emotes.append(e['name'].lower().replace(broadcaster,''))

for i in emotes:
    print('    - '+i)
