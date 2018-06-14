from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	return "placeholder while everything is set up"


