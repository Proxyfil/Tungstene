<img src="https://media.discordapp.net/attachments/874044700309454858/951559814654357574/banner.png" width="600" height="300">

# Chrono-Break Roadmap
### We build data visualisation future here.
##### Project by : Proxyfil and Dragonfyr

***

## What's this project ?

This project is intended to be a new era for data-visualisation.
The main goal is to produce large amount of data about Twitch during some defined time on multiple channels (like for charity event).

We want to go beyond viewer count and money earned. We want to show community moves, how it evolves during an event and how much these can change (at least for some time) the form of the platform.

We will focus on IRC channel that provide a lot of data about users connected, what is said, and more such as presence for streamers and viewers. We will find out the best way to show the diversity of Twitch through open-data.

***

## Why this could be a game-changer ?

Today many events can't really understand their impact on community. We can only see the result but with open data we can mesure this impact on the platform.

We can understand viewers, what they like, who they watch, for which reason. We can associate all these data to help events to grow.

***

## Logs

```diff
[07/03/2022]
+ First writting, setup project and looking for objectives

[08/03/2022]
+ Project confirmed, starting thinking about it
+ MD adds and corrections

[10/03/2022]
+ Replit adaptation

[16/03/2022]
+ Website dev
```

***

## To do list

- Main Program
- Compression Algorythm
- TwitchAPI Getter
- TwitchIRC Getter
- FrontEnd Website
- BackEnd Website

---

## Techs

- DB : json
- Web : React + Framework (materialUI ?) + Node (Express for API)
- Scripts : Python

---

## Data collected (where)

- IRC Twitch
- API Twitch
- Unofficial API (TwitchTracker)

---

## Workflow

### Proxyfil
- Backend Web
- API
- Host
- Requests to APIs

### Dragonfyr
- DB (organisation, syntax)
- GUI ?


### Together
- Frontend Web
- Global Program
- Algorythms

---

## Parts
- Tungstene (data collection)
- Rhodium (data display)
***

## Files

- **[F] Thungstene** 
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
  - [f] tungstene.py
  - [f] config.yml
  - [f] README.md
- **[F] Rhodium**
  - **[F] -- **


***
