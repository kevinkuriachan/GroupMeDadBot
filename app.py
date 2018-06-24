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

# Classes for bots:

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

class DadBot(Bot):
	def __init__(self, BOT_ID):
		super().__init__(BOT_ID)

	def SendDadJoke(self):
		jokesList = open('dadjokes.txt','r').readlines()
		joke = random.choice(jokesList).strip('\n')
		self.SendMessage(joke)

	def SendDadMessage(self, msgRec):
		msgSend = ""
		if ("I'm" in msgRec):
		    start = msgRec.find("I'm") + 4
		    name = ""
		    for index in range(start, len(msgRec)):
		        if msgRec[index] == ".":
		            break
		        name = name+msgRec[index]
		    msgSend = "Hi " + name + ", I'm Dad."
		elif ("I’m" in msgRec):
		    start = msgRec.find("I’m") + 4
		    name = ""
		    for index in range(start, len(msgRec)):
		        if msgRec[index] == ".":
		            break
		        name = name+msgRec[index]
		    msgSend = "Hi " + name + ", I'm Dad."
		if msgSend != "":	
			self.SendMessage(msgSend)


class MockBot(Bot):
	def __init__(self, BOT_ID, name):
		super().__init__(BOT_ID)

	def Mock(self, data):
		if data['name'] == self.name:
			msg = ''
			zeroOrOne = random.randint(0,1)
			for index in range(len(preCap)):
				if (index%2 == zeroOrOne):
					msg = msg+preCap[index].lower()
				else:
					msg = msg+preCap[index].upper()
			self.SendMessage(msg)
		
class EchoBot(Bot):
	def __init__(self, BOT_ID):
		super().__init__(BOT_ID)

	def EchoMsg(data):
		if data['name'] != 'Mock Bot':
			msg = '{} sent "{}".'.format(data['name'], data['text'])
			self.SendMessage(msg)


#create a route for each bot

@app.route('/')
def rootPage():
	return "GroupMe bots code located at 'github.com/kevinkuriachan/GroupMeDadBot'"


@app.route('/dadbot', methods=['POST'])
def dadBotFunc():
	data = request.get_json()
	if (data['name'] == 'DadBot'):
		return ok, 200
	dadBot = DadBot(GROUPME_DADBOT_ID)
	print(data)
	dadBot.SendDadMessage(data['text'])
	if "@DadBot" in data['text']:
		dadBot.SendDadJoke()

	return "ok", 200


@app.route('/colbymockbot', methods=['POST'])
def colbyMockBotFunc():
	data = request.get_json()
	if data['name'] == 'Colby Mock Bot':
		return ok, 200
	colbyMockBot = MockBot(GROUPME_COLBYBOT_ID, 'Colby Lorenz')
	colbyMockBot.Mock(data)

	return "ok", 200

