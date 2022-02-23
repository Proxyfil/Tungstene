import json
import os
import datetime

def compression(input_file,compress_type):
    if(compress_type == "simple"):
        compression_t1(input_file)
    else:
        return("[ERROR] An error occured")

def compression_t1(input_file):
    file_path = "./data/"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+"/"

    os.mkdir(file_path)
    viewers_list = {}
    label_list = {}
    id = 0

    name_to_id = {}
    viewers = {"nodes": {}, "links": {}} #Viewers to Alt
    alt = {"nodes": {}, "links": {}} #Alt to Viewers
    mother = {"nodes": [], "links": []} #Alt and Streamers

    file = json.loads(input_file) #Load file
    for streamer in file.keys(): #For each streamer in the keys of the file
        for viewer in file[streamer]: #For each viewer of this streamer
            if(viewer not in name_to_id.keys()): #If viewer is not registered
                name_to_id[viewer] = hex(id)[2:] #Hex number ID
                id += 1
            
            if(viewer in viewers_list.keys()): #If viewer registered with his streamers
                viewers_list[viewer].append(streamer) #Add this streamer
            else:
                viewers_list[viewer] = [streamer] #Set this streamer

    for key in viewers_list.keys(): #For viewer in keys
        if " | ".join(viewers_list[key]) not in label_list.keys(): #If streamers label of this viewer not already registered
            label_list[" | ".join(viewers_list[key])] = [key] #Set label with viewer in it
            alt["nodes"][" | ".join(viewers_list[key])] = [{"id":name_to_id[key],"type":"viewer"}] #Set viewer as child-node of this alt
        else:
            label_list[" | ".join(viewers_list[key])].append(key) #Add viewer to label_list with label as id
            alt["nodes"][" | ".join(viewers_list[key])].append({"id":name_to_id[key],"type":"viewer"}) #Add viewer as child-node of this alt

    #Build mother
    #Write File

with open("./data/global_map.json","r") as f:
    compression(f.read(),"simple")

    