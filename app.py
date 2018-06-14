from flask import Flask, request
import os
import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen

app = Flask(__name__)

@app.route('/', methods=['POST'])
def echoMsg():
	data = request.get_json()

	if data['name'] != 'EchoBot':
		msg = '{}, you sent"{}".'.format(data['name'], data['text'])
		sendMessage(msg)

	return "ok", 200

def sendMessage(msg):
	url = 'https://api.groupme.com/v3/bots/post'
	
	data = {
			'bot_id' : os.getenv('GROUPME_DADBOT_ID'),
			'text' : msg,
			}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()