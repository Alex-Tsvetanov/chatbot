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

bot.train('chatterbot.corpus.english')
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
		response.set_cookie('c', '[]');
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
