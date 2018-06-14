from flask import Flask, request
import os
import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen

app = Flask(__name__)

@app.route('/', methods=['POST'])
def bot_func():
	data = request.get_json()

	if data['name'] != 'EchoBot':
		sendMock(data, 'Kevin Kuriachan')

	return "ok", 200

def echoMsg(data):
	if data['name'] != 'EchoBot':
		msg = '{}, you sent "{}".'.format(data['name'], data['text'])
		return msg

def sendMessage(msg):
	url = 'https://api.groupme.com/v3/bots/post'
	
	data = {
			'bot_id' : os.getenv('GROUPME_DADBOT_ID'),
			'text' : msg,
			}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()

def pureEcho(data)
	return data['text']

def mock(data, name):
	if data['name'] == name:
		preCap = data['text']
		msg = ''
		for index in range(len(preCap)):
			if (index%2 == 0):
				msg = msg+preCap[index].lower()
			else:
				msg = msg+preCap[index].upper()
		return msg

def sendMock(data,name):
	if(data['name']==name):
		msg = mock(data)
		msgData = {
					'bot_id' : os.getenv('GROUPME_DADBOT_ID'),
					'text' : msg,
					'attachments': [{'type':'image', 'image_url': 'https://pbs.twimg.com/media/C_bTGQlUwAAwoAM.jpg'}]
					}
		url = 'https://api.groupme.com/v3/bots/post'
		request = Request(url, urlencode(data).encode())
		json = urlopen(request).read().decode()