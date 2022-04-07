import json
import os


def read(file):
	data = open(file,'r',encoding='utf-8')
	content = ''
	for char in data:
		content += char
	return json.loads(content)