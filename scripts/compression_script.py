import json

def compression(input_file,compress_type):
    if(compress_type == "simple"):
        compression_t1(input_file)
    else:
        return("[ERROR] An error occured")

def compression_t1(input_file):
    viewers = {}
    compressed_file = {}
    compressed_viewers = {}
    compressed_streamers = {}

    file = json.loads(input_file)
    for streamer in file.keys():
        for viewer in file[streamer]:
            if viewer in viewers.keys():
                viewers[viewer].append(streamer)
            else:
                viewers[viewer] = [streamer]

    for viewer in viewers.keys():
        label = " | "
        for streamer in viewers[viewer]:
            label += streamer+" | "
        for streamer in viewers[viewer]:
            if(streamer in compressed_streamers.keys()):
                compressed_streamers[streamer].append(label)
            else:
                compressed_streamers[streamer] = [label]

        if(label in compressed_viewers.keys()):
            compressed_viewers[label].append(viewer)