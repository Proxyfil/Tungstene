<img src="../design/banner.png" width="600" height="300">

# Chrono-Break Roadmap
### We build data visualisation future here.
##### Project by : Pierre-Louis Leclerc and Ugo Peduzzi

***

## What's this project ?

This project is intended to be a new era for data-visualisation.
The main goal is to produce large amount of data about Twitch during some define time on multiple channels (like for charity event).

We want to go beyond viewer count and money earn. We want to show community moves, how it evolve during an event and how much these can change (at least for some time) the form of the platform.

We will focus on IRC channel that provide many data about users connected, what is said as like as presence for streamers and viewers. We will find out the best way to show the diversity of Twitch throught open-data.

***

## Why this could be a game-changer ?

Today many events can't really understand their impact on community. We can only see the result but with open data we can mesurate this impact on the platform.

We can understand viewers, what they like, who they watch, for which reason. We can associate all these data to help events to grow.

***

## Logs

```diff
[07/03/2022]
+ First writting, setup project and looking for objectives
```

***

## To do list

- Main Program
- Compression Algorythm
- TwitchAPI Getter
- TwitchIRC Getter
- FrontEnd Website
- BackEnd Website

***

## Files

- **[F] data** `(Not intended to be opened by users)`
    - [F] {date_of_scan}
        - [f] global_map.json
        - [f] viewers_data.json
        - [f] streamers_data.json
- **[F] scripts** `(Not intended to be opened by users)`
    - [f] cb_compression.py
    - [f] cb_data_twitch.py
- **[F] output** `(Intended to be opened by users)`
    - [F] {date_of_scan}
        - [f] api.json

***
