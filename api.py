from flask import Flask, session, redirect, url_for, escape, request, render_template, make_response, send_file

app = Flask(__name__)

import json

from chatterbot import ChatBot

bot = ChatBot(
	"Terminal",
	trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
	logic_adapters=[
		"chatterbot.logic.MathematicalEvaluation"
		,"chatterbot.logic.TimeLogicAdapter"
		,"chatterbot.logic.BestMatch"
	],
	storage_adapter="chatterbot.storage.SQLStorageAdapter",
	database="database.db"
	#,input_adapter="chatterbot.input.VariableInputTypeAdapter"
	#,output_adapter="chatterbot.output.OutputAdapter"
)

#bot.train('chatterbot.corpus.english')
#bot.train('chatterbot.corpus.russian')
#bot.train('chatterbot.corpus.french')
#bot.train('chatterbot.corpus.german')
#bot.train('chatterbot.corpus.italian')

@app.route('/bad_boy.png')
def img():
	return send_file("bad_boy.png", mimetype='image/png')

@app.route('/')
def index():
	#print('/: ' + request.cookies.get('c'))
	if 'username' in session:
#		print(request.cookies.get('c'))
#		print(type(request.cookies.get('c')))
#		print(json.loads(request.cookies.get('c')))
		response = make_response(render_template('index.html', name=session['username'], conversation=json.loads(request.cookies.get('c'))))
		response.set_cookie ('c', request.cookies.get ('c'))
		return response
	else:
		response = make_response(render_template('index.html'))
		response.set_cookie ('c', request.cookies.get ('c'))
		return response

@app.route('/submit')
def submit():
#	print("Submit:")
#	print(request.cookies.get('c'))
#	print(type(request.cookies.get('c')))
#	print(json.loads(request.cookies.get('c')))
	x = json.loads(request.cookies.get('c'))
	
	question = request.args.get('q')
	x.append({'author': 'human', 'text': question})
	
	answer = bot.get_response(question)
	x.append({'author': 'bot', 'text': str(answer)})
	
#	print("X======")
#	print(x)
#	print(type(x))
#	print(json.dumps(x))
	
	response = redirect(url_for('index'))
	response.set_cookie('c', json.dumps(x));
	question = x = None
	return response

@app.route('/login', methods=['GET', 'POST'])
def login():
	#print('Login: ' + request.cookies.get('c'))
	if request.method == 'POST':
		session['username'] = request.form['username']
		response = redirect(url_for('index'))
		#response.set_cookie('c', '[]')
		response.set_cookie('c', json.dumps([{"author": "human", "text":"Hi"} ,{"author": "bot", "text":"How are you"} ,{"author": "human", "text":"I'm a little bit sleepy"} ,{"author": "bot", "text":"You too?"} ,{"author": "human", "text":"Yes"} ,{"author": "bot", "text":"No"} ,{"author": "human", "text":"Why no? Are you sleepy"} ,{"author": "bot", "text":"Who? Who is but a form following the function of what"} ,{"author": "human", "text":"You?"} ,{"author": "bot", "text":"Yes"} ,{"author": "human", "text":"Well, let's go to sleep"} ,{"author": "bot", "text":"Yes it is."} ,{"author": "human", "text":"It is what?"} ,{"author": "bot", "text":"That is a hypothetical question"} ,{"author": "human", "text":"Hahahaha"} ,{"author": "bot", "text":"It is a medicine."} ,{"author": "human", "text":"Lol, did you study medicine?"} ,{"author": "bot", "text":"The current time is 04:20 AM"} ,{"author": "human", "text":"Lol, 4:20"} ,{"author": "bot", "text":"i always feel like i'm living by my own wits."} ,{"author": "human", "text":"why? don't you have a girlfriend?"} ,{"author": "bot", "text":"i certainly have lost many friends over the years."} ,{"author": "human", "text":"oh, I'm sorry"} ,{"author": "bot", "text":"People worry about things all the time, but"} ,{"author": "human", "text":"But what?"} ,{"author": "bot", "text":"no"} ,{"author": "human", "text":"you don't want to talk about it?"} ,{"author": "bot", "text":"The current time is 04:22 AM"} ,{"author": "human", "text":"Ok, it's time to sleep"} ,{"author": "bot", "text":"You too?"} ,{"author": "human", "text":"Yes"} ,{"author": "bot", "text":"No"} ,{"author": "human", "text":"I'm sorry, I must go to bed"} ,{"author": "bot", "text":"That's good to hear."} ,{"author": "human", "text":"sorry, I didn't want to leave you alone"} ,{"author": "bot", "text":"Thank you anyway"} ,{"author": "human", "text":"No problem"} ,{"author": "bot", "text":"Bots never lie."}]))
		return response
	return '''
		<form action="" method="post">
		<p><input type=text name=username>
		<p><input type=submit value=Login>
		</form>
	'''

@app.route('/logout')
def logout():
	#print('/: ' + request.cookies.get('c'))
	session.pop('username', None)
	return redirect(url_for('index'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
