#Imports
import requests
import time
import yaml
import json

#Variables Declarements
config_file = "config.yml"

#Functions Declarement
def api_requests(channel):
    r = requests.get('https://tmi.twitch.tv/group/user/'+channel+'/chatters')
    return r.json()["chatters"]["viewers"]

def verification(database,resp,channel):
    if(channel in database.keys()):
            for viewer in resp:
                if(viewer not in database[channel]):
                    database[channel].append(viewer)
    else:
        database[channel] = resp

    return database

def read(file):
    data = open(file,"r",encoding="utf-8")
    content = ""
    for char in data:
        content += char
    return json.loads(content)

def write(file,data):
    database_file = open(file,"w",encoding="utf-8")
    json.dump(data, database_file, indent = 4)
    database_file.close()

def display_init():
    print(" ______                                 __                            \n/\__  _\                               /\ \__                         \n\/_/\ \/ __  __    ___      __     ____\ \ ,_\    __    ___      __   \n   \ \ \/\ \/\ \ /' _ `\  /'_ `\  /',__\\ \ \/  /'__`\/' _ `\  /'__`\ \n    \ \ \ \ \_\ \/\ \/\ \/\ \L\ \/\__, `\\ \ \_/\  __//\ \/\ \/\  __/ \n     \ \_\ \____/\ \_\ \_\ \____ \/\____/ \ \__\ \____\ \_\ \_\ \____\ \n      \/_/\/___/  \/_/\/_/\/___L\ \/___/   \/__/\/____/\/_/\/_/\/____/\n                            /\____/                                   \n                            \_/__/                                    \n")

def file_constructor(file):
    logins = []
    nodes = []
    links = []
    data = read(file)

    for streamer in data.keys():
        logins.append(streamer)
        nodes.append({"id": streamer, "type": "streamer"})
        for viewer in data[streamer]:
            if viewer not in logins:
                logins.append(viewer)
                nodes.append({"id": viewer, "type": "viewer"})
            links.append({"source": viewer, "target": streamer})

    write(config["output"]["nodes"],nodes)
    write(config["output"]["links"],links)
    print(f"[LOGS] Output files written. Total users registered : {len(logins)}")

def main():
    display_init()
    print(f"[WARMUP] Starting every protocols...")
    print(f"[WARMUP] Config file as {config_file}")

    config_yml = open(config_file,"r",encoding="utf-8")
    config = yaml.load(config_yml, Loader=yaml.loader.SafeLoader)

    if(config["requests"]["start"]-time.time() < 0):
        print("[ERROR] Start timestamp is in the past. Setting start time in 1 second")
        config["requests"]["start"] = time.time()+1

    if(config["requests"]["start"]-time.time() > config["requests"]["end"]-time.time()):
        print("[ERROR] Start timestamp is after End Timestamp... You can't do this :/")
        exit()

    database = read("global_map.json")

    display_temp = config["requests"]["start"]-time.time()
    display_temp_global = time.gmtime(config["requests"]["start"])
    print(f"[WARMUP] Starting in {display_temp} seconds (or {display_temp_global[3]+1}:{display_temp_global[4]}:{display_temp_global[5]} {display_temp_global[2]}/{display_temp_global[1]}/{display_temp_global[0]} UTC+1)")
    time.sleep(config["requests"]["start"]-time.time())

    display_temp = config["requests"]["end"]-time.time()
    display_temp_global = time.gmtime(config["requests"]["end"])
    print(f"[LOGS] Starting Protocols --- Ending in {display_temp} seconds (or {display_temp_global[3]+1}:{display_temp_global[4]}:{display_temp_global[5]} {display_temp_global[2]}/{display_temp_global[1]}/{display_temp_global[0]} UTC+1)")

    while(time.time() < config["requests"]["end"]):
        for channel in config["requests"]["streamers"]:
            resp = api_requests(channel)
            database = verification(database,resp,channel)
        write("global_map.json",database)

        print(f"[LOGS] Everything went right. Waiting for next scan")
        time.sleep(config["requests"]["delay"])

    print(f"[LOGS] Query ended due to time limit")

    file_constructor("global_map.json")
    print(f"[EXIT] Program ended due to end of process")

    

    
if __name__ == "__main__":
    main()