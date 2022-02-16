# Tungstene
Python Script to get every users connected to a chat Twitch. 
Part of Chrono-Break Project

## Requirements
 - **pyyaml** python lib for reading config file
 - **twitchAPI** python lib for accessing twitch api data

## Usage
### *config.yml* is the default configuration file you can edit it like so :
- *requests* is the sub-part dedicated to requests params
    - *delay* define the time to wait between requests **(in ms)**
    - *start* in seconds after epoch (Unix) to begin the scan
    - *end* in seconds after epoch (Unix) to end the scan
- *output* is the sub-part dedicated to output file params
    - *nodes* is the name of the nodes file
    - *links* is the name of the links file
- *scan* is the sub-part dedicated to twitch requests params
    - *game_id* is set as twitch game id (can be browse by making *scan* like this : **- game_id : "" - language : "" - streamers : false**)
    - *language* is usually 2 letters code for twitch (ex : **fr**,**en**,**es**,**de**)
    - *top_lenght* is the number of streamers from the top you want to query (not useful when you define streamer list)
    - *streamers* contain the list of streamers logins you want to track
- *creds* is the sub-part dedicated to tokens **Never Reveal This**
    - *id_twitch* is the id of your application (provided by Twitch)
    - *secret_twitch* is the secret key of your application (provided by Twitch)