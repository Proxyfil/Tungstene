import requests
import time
#import yaml
import json
#from twitchAPI.twitch import Twitch
import os
from datetime import datetime

def read(file):
	data = open(file,'r',encoding='utf-8')
	content = ''
	for char in data:
		content += char
	return json.loads(content)


def sum_viewer(mode) : #nb viewer for 1 channel / all for 1 scan
	database = read('./data/viewtime.json')
	dict_view = {}
	for streamer in database.keys() :
		if mode == 'all' :
			for i in database[streamer].keys() :
				dict_view[i] = ''
	if mode not in database.keys() :
		return "[Error] Streamer not in Database"
	else :
		for i in database[mode].keys() :
			dict_view[i] = ''
	return len(dict_view)

def sum_chatter(mode) : #nb chatter for 1 channel / all for 1 scan
	database = read('./data/tchat_messages.json')
	dict_chat = {}
	for streamer in database.keys() :
		if mode == 'all' :
			for i in database[streamer].keys() :
				dict_chat[i] = ''
	if '#'+mode not in database.keys() :
		return "[Error] Streamer not in Database"
	else :
		for i in database['#'+mode].keys() :
			dict_chat[i] = ''
	return len(dict_chat)

def top_viewer(mode) : #Best viewer for 1 channel / all
	database = read('./data/viewtime.json')
	ls_view = {}
	max = 0
	view = []
	for streamer in database.keys() :
		if mode == 'all' :
			for i in database[streamer].keys() :
				if i in ls_view :
					ls_view[i] += database[streamer][i]
				else :
					ls_view[i] = database[streamer][i]
	if mode not in database.keys():
		return "[Error] Streamer not in Database"
	else :
		for i in database[mode].keys() :
			ls_view[i] = database[mode][i]
	for i in ls_view.keys() :
		view.append((i,ls_view[i]))
	view.sort()
	return (view)
			
def top_chatter(mode) : #Best chatter for 1 channel / all
	database = read('./data/tchat_messages.json')
	ls_chat = {}
	max = 0
	chat = ''
	for streamer in database.keys() :
		if mode == 'all' :
			for i in database[streamer].keys() :
				if i in ls_chat :
					ls_chat[i] += database[streamer][i]
				else :
					ls_chat[i] = database[streamer][i]
	if '#'+mode not in database.keys():
		return "[Error] Streamer not in Database"
	else :
		for i in database['#'+mode].keys() :
			ls_chat[i] = database[streamer][i]
	for i in ls_chat.keys() :
		if ls_chat[i] > max :
			chat = i
			max = ls_chat[i]
	return (chat, max)
def time_streamer(mode) :#Time watched for 1 channel / all / Best of the channels scanned
	a=1
print(top_viewer('zerator'))