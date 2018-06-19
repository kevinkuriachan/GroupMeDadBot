from flask import Flask, request
import os
import json
import random

from urllib.parse import urlencode
from urllib.request import Request, urlopen

app = Flask(__name__)

#set the bot id's of each bot from environment variables:

GROUPME_DADBOT_ID = os.getenv('GROUPME_DADBOT_ID')
GROUPME_COLBYBOT_ID = os.getenv('GROUPME_COLBYBOT_ID')


#create a route for each bot

@app.route('/', methods=['POST'])
def bot_func():
	data = request.get_json()

	if data['name'] != 'Colby Mock Bot':
		sendMockColby(data, 'Colby Lorenz')

	if data['name'] != 'DadBot':
		sendDadMsg(data)

	return "ok", 200


@app.route('/dadbot', methods=['POST'])
def dadBotFunc():



	return ok, 200


@app.route('/colbymockbot', methods=['POST'])
def colbyMockBotFunc():



	return ok, 200




def echoMsg(data):
	if data['name'] != 'Mock Bot':
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

def pureEcho(data):
	return data['text']

def mock(data):
	preCap = data['text']
	msg = ''
	zeroOrOne = random.randint(0,1)
	for index in range(len(preCap)):
		if (index%2 == zeroOrOne):
			msg = msg+preCap[index].lower()
		else:
			msg = msg+preCap[index].upper()
	return msg

def sendMock(data, name):
	if(data['name']==name):
		msg = mock(data)
		msgData = {
					'bot_id' : os.getenv('GROUPME_DADBOT_ID'),
					'text' : msg
					}
		url = 'https://api.groupme.com/v3/bots/post'
		request = Request(url, urlencode(msgData).encode())
		json = urlopen(request).read().decode()


def sendMockColby(data, name):
	if(data['name']==name):
		msg = mock(data)
		msgData = {
					'bot_id' : os.getenv('GROUPME_COLBYBOT_ID'),
					'text' : msg,
					}
		url = 'https://api.groupme.com/v3/bots/post'
		request = Request(url, urlencode(msgData).encode())
		json = urlopen(request).read().decode()


def getDadMsg(data):
	msgRec = data['text']
	msgSend = ""
	if ("I'm" in msgRec):
	    start = msgRec.find("I'm") + 4
	    print("in loop")
	    name = ""
	    for index in range(start, len(msgRec)):
	        if msgRec[index] == ".":
	            break
	        name = name+msgRec[index]
	        print(name)
	    msgSend = "Hi " + name + ", I'm Dad."
	elif ("I’m" in msgRec):
	    start = msgRec.find("I’m") + 4
	    print("in loop")
	    name = ""
	    for index in range(start, len(msgRec)):
	        if msgRec[index] == ".":
	            break
	        name = name+msgRec[index]
	        print(name)
	    msgSend = "Hi " + name + ", I'm Dad."

	return msgSend

def sendDadMsg(data):
	if ("I'm" in data['text']):
		url = 'https://api.groupme.com/v3/bots/post'
		
		msg = getDadMsg(data)

		data = {
				'bot_id' : os.getenv('GROUPME_DADBOT_ID'),
				'text' : msg,
				}
		request = Request(url, urlencode(data).encode())
		json = urlopen(request).read().decode()

	elif ("I’m" in data['text']):
		url = 'https://api.groupme.com/v3/bots/post'
		
		msg = getDadMsg(data)

		data = {
				'bot_id' : os.getenv('GROUPME_DADBOT_ID'),
				'text' : msg,
				}
		request = Request(url, urlencode(data).encode())
		json = urlopen(request).read().decode()





class Bot:
	def __init__(self, BOT_ID):
		self.BOT_ID = BOT_ID

	def SendMessage(self, message):
		url = 'https://api.groupme.com/v3/bots/post'
	
		data = {
				'bot_id' : self.BOT_ID,
				'text' : message,
				}
		request = Request(url, urlencode(data).encode())
		json = urlopen(request).read().decode()



dadBot = Bot(GROUPME_DADBOT_ID)
