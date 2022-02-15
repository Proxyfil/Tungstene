# Tungstene
Python Script to get every users connected to a chat Twitch. 
Part of Chrono-Break Project

## Requirements
 - **pyyaml** python lib for reading config file

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
    - *game_id*
    - *language*
    - *top_lenght*
    - *streamers* contain the list of streamers logins you want to track
- *creds* is the sub-part dedicated to tokens **Never Reveal This**
    - *id_twitch* is the id of your application (provided by Twitch)
    - *secret_twitch* is the secret key of your application (provided by Twitch)