# Tungstene
Python Script to get every users connected to a chat Twitch. 
Part of Chrono-Break Project

## Requirements
 - **pyyaml** python lib for reading config file

## Usage
### *config.yml* is the default configuration file you can edit it like so :
- *requests* is the sub-part dedicated to requests params
    - *streamers* contain the list of streamers logins you want to track
    - *delay* define the time to wait between requests **(in ms)**
    - *start* in seconds after epoch (Unix) to begin the scan
    - *end* in seconds after epoch (Unix) to end the scan