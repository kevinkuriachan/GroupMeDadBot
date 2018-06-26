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
GROUPME_FAM_DAD_ID = os.getenv('GROUPME_FAM_DAD_ID')

# Classes for bots:

class Bot:
	def __init__(self, BOT_ID, name):
		self.BOT_ID = BOT_ID
		self.name = name

	def SendMessage(self, message):
		url = 'https://api.groupme.com/v3/bots/post'
	
		data = {
				'bot_id' : self.BOT_ID,
				'text' : message,
				}
		request = Request(url, urlencode(data).encode())
		json = urlopen(request).read().decode()

class DadBot(Bot):
	def __init__(self, BOT_ID, name):
		super().__init__(BOT_ID, name)

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
	def __init__(self, BOT_ID, name, nameToMock):
		super().__init__(BOT_ID, name)
		self.nameToMock = nameToMock
	def Mock(self, data):
		if data['name'] == self.nameToMock:
			msgOrig = data['text']
			msg = ''
			zeroOrOne = random.randint(0,1)
			for index in range(len(msgOrig)):
				if (index%2 == zeroOrOne):
					msg = msg+msgOrig[index].lower()
				else:
					msg = msg+msgOrig[index].upper()
			self.SendMessage(msg)
		
class EchoBot(Bot):
	def __init__(self, BOT_ID, name):
		super().__init__(BOT_ID, name)

	def EchoMsg(data):
		if data['name'] != 'Mock Bot':
			msg = '{} sent "{}".'.format(data['name'], data['text'])
			self.SendMessage(msg)


#create an instance and route for each bot

@app.route('/')
def rootPage():
	return "GroupMe bots code located at 'github.com/kevinkuriachan/GroupMeDadBot'"

testDadBot = DadBot(GROUPME_DADBOT_ID, 'DadBot')
testDadBotActive = True
@app.route('/dadbot', methods=['POST'])
def dadBotFunc():
	data = request.get_json()
	if (data['name'] == testDadBot.name):
		return "ok", 200
	msg = data['text']
	if "@DadBot toggle" in msg:
		testDadBotActive = not testDadBotActive
		if (testDadBotActive):
			msgToSend = "DadBot Active"
		else:
			msgToSend = "DadBot Disabled"
		testDadBot.SendMessage(msgToSend)
	if not testDadBotActive:
		return "ok", 200	
	testDadBot.SendDadMessage(data['text'])
	if "@DadBot" in data['text']:
		testDadBot.SendDadJoke()

	return "ok", 200

colbyMockBot = MockBot(GROUPME_COLBYBOT_ID, 'Colby Mock Bot', 'Colby Lorenz')
mockOrNo = True
@app.route('/colbymockbot', methods=['POST'])
def colbyMockBotFunc():
	data = request.get_json()
	if data['name'] == colbyMockBot.name:
		return "ok", 200
	msg = data['text']
	if "@MockBot toggle" in msg:
		mockOrNo = not mockOrNo
		if (mockOrNo):
			msgToSend = "Mock Bot Active"
		else:
			msgToSend = "Mock Bot Disabled"
		colbyMockBot.SendMessage(msgToSend)
	if not mockOrNo:
		return "ok", 200
	colbyMockBot.Mock(data)

	return "ok", 200


famDadBot = DadBot(GROUPME_FAM_DAD_ID, DadBot)
@app.route('/nerdvalley', methods=['POST'])
def nerdValley():
	data = request.get_json()
	if (data['name'] == famDadBot.name):
		return "ok", 200	
	famDadBot.SendDadMessage(data['text'])
	if "@DadBot" in data['text']:
		famDadBot.SendDadJoke()

	return "ok", 200