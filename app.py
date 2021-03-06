from flask import Flask, request
import os
import json
import random
import praw
import pickle
import urllib
import groupy
from groupy.client import Client, attachments

from urllib.parse import urlencode
from urllib.request import Request, urlopen

app = Flask(__name__)

#set the bot id's of each bot from environment variables:

GROUPME_DADBOT_ID = os.getenv('GROUPME_DADBOT_ID')
GROUPME_COLBYBOT_ID = os.getenv('GROUPME_COLBYBOT_ID')
GROUPME_FAM_DAD_ID = os.getenv('GROUPME_FAM_DAD_ID')
GROUPME_HOWDYBOT_ID = os.getenv('GROUPME_HOWDYBOT_ID')
TOKEN = os.getenv('GM_TOKEN')

#creating a reddit instance

reddit = praw.Reddit(client_id = os.getenv('redditID'), client_secret = os.getenv('redditSecret'), user_agent = 'my user agent')

GMClient = Client.from_token(TOKEN)


def getGMData(gm_id):
	url = 'https://api.groupme.com/v3/groups?token='+TOKEN
	response = urllib.request.urlopen(url)
	html = response.read()
	info = html.decode('utf8')
	data = json.loads(info)
	for item in data['response']:
		if item['group_id'] == gm_id:
			return item

def getUserID(item, username):
	for person in item['members']:
		if (person['nickname'] == username):
			return person['user_id']

# Classes for bots:

class Bot:

	
	## TODO: find a way to add persistence to characteristics across multiple runs of the app
	isActive = True

	def saveStatus(self):
		with open(self.BOT_ID+"Status.pkl", "wb") as file:
				pickle.dump(self, file)

	def loadStatus(self):
		if(os.path.isfile(self.BOT_ID+"Status.pkl")):
			with open(self.BOT_ID+"Status.pkl", "rb") as file:
				obj = pickle.load(file)
			if obj.isActive == False:
				self.isActive = False
		else:
			 self.saveStatus()

	def __init__(self, BOT_ID, name):
		self.BOT_ID = BOT_ID
		self.name = name
		self.isActive = True
		self.loadStatus()

	def SendMessage(self, message):
		url = 'https://api.groupme.com/v3/bots/post'
	
		data = {
				'bot_id' : self.BOT_ID,
				'text' : message,
				}
		request = Request(url, urlencode(data).encode())
		json = urlopen(request).read().decode()

	def Mention(self, name, id_):
		url = 'https://api.groupme.com/v3/bots/post'
		text = "@"+name
		mention = attachments.Mentions([[0, len(text)]], user_ids = [id_])
		GMClient.bots.post(self.BOT_ID, text, [mention])
		
	def Deactivate(self):
		self.isActive = False
		self.saveStatus()
		self.SendMessage(self.name+" disabled")
	def Active(self):
		self.isActive = True
		self.saveStatus()
		self.SendMessage(self.name+" enabled") 

	def Toggle(self):
		if self.isActive:
			self.Deactivate()
		else:
			self.Active()

class DadBot(Bot):
	def __init__(self, BOT_ID, name):
		super().__init__(BOT_ID, name)

	def SendDadJokeFromList(self):
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

	def SendDadJokeFromReddit(self): # picks a random hot post from r/dadjokes
		submissions = list(reddit.subreddit('dadjokes').hot(limit=150))
		submission = random.choice(submissions)
		msg = submission.title
		acceptableEnds = ['.', ':', '?', '!']
		if (msg[-1] not in acceptableEnds):
			msg = msg+"."
		msg = msg+ " " +submission.selftext
		self.SendMessage(msg)

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


class IntroBot(Bot):
	def __init__(self, BOT_ID, name):
		super().__init__(BOT_ID, name)

	msgCount = 0

	def Intro(self, name):
		msg = "Howdy {}! Welcome to the LechFadden community! We need to know a couple things so we can get you situated. Who is your SA parent and what dorm/floor are you on? Beep Boop. Ts&Gs!!!".format(name)
		self.SendMessage(msg)

	def PayRespect(self):
		msg = "F"
		self.SendMessage(msg)

@app.route('/')
def rootPage():
	return "GroupMe bots code located at 'github.com/kevinkuriachan/GroupMeDadBot'"

introBot = IntroBot(GROUPME_HOWDYBOT_ID, 'HowdyBot')
@app.route('/LFjoin', methods=['POST'])
def introFunc():
	data = request.get_json()
	if (data['name'] == introBot.name):
		return "ok", 200
	#print(data)
	gm_id = data['group_id']
	gm_info = getGMData(gm_id)

	if(data['name'] == 'GroupMe'):
		if ("has joined the group" in data['text']):
			name = data['text'].replace(" has joined the group", "")
			nameList = name.split(" ",1)
			introBot.Intro(nameList[0])
			user_id = getUserID(gm_info, name)
			print(user_id)
			introBot.Mention(name, user_id)
			
		if (("added" in data['text']) and ("to the group" in data['text'])):
			stri = data['text']
			name = stri[(stri.find("added")+6):].replace(" to the group.", "")
			nameList = name.split(" ",1)
			introBot.Intro(nameList[0])
			user_id = getUserID(gm_info, name)
			print(user_id)
			introBot.Mention(name, user_id)

		if (("removed" in data['text']) and ("from the group" in data['text'])):
			introBot.PayRespect()

	return "ok", 200

testDadBot = DadBot(GROUPME_DADBOT_ID, 'DadBot')
@app.route('/dadbot', methods=['POST'])
def dadBotFunc():
	data = request.get_json()
	print(data)
	if (data['name'] == testDadBot.name):
		return "ok", 200
	msg = data['text']
	if "@DadBot toggle" in msg:
		testDadBot.Toggle()
		return "ok", 200
	if not testDadBot.isActive:
		return "ok", 200	
	testDadBot.SendDadMessage(data['text'])
	if ("@DadBot" in data['text']) and ("toggle" not in data['text']):
		testDadBot.SendDadJokeFromReddit()

	if ("test mention" in data['text']):
		testDadBot.Mention("Kevin", data['sender_id'], "test mention")


	return "ok", 200

colbyMockBot = MockBot(GROUPME_COLBYBOT_ID, 'Colby Mock Bot', 'Colby Lorenz')
@app.route('/colbymockbot', methods=['POST'])
def colbyMockBotFunc():
	colbyMockBot.isActive = False
	data = request.get_json()
	if data['name'] == colbyMockBot.name:
		return "ok", 200
	msg = data['text']
	if "@MockBot toggle" in msg:
		colbyMockBot.Toggle()
	if not colbyMockBot.isActive:
		return "ok", 200
	colbyMockBot.Mock(data)

	return "ok", 200


famDadBot = DadBot(GROUPME_FAM_DAD_ID, 'DadBot')
@app.route('/nerdvalley', methods=['POST'])
def nerdValley():
	data = request.get_json()
	if (data['name'] == famDadBot.name):
		return "ok", 200	
	#famDadBot.SendDadMessage(data['text'])
	if "@DadBot" in data['text']:
		famDadBot.SendDadJokeFromReddit()

	return "ok", 200