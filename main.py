# -*- coding: utf-8 -*-
from chatterbot import ChatBot


bot = ChatBot(
    "Amon",
	trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation"
		,"chatterbot.logic.TimeLogicAdapter"
		,"chatterbot.logic.BestMatch"
    ],
    input_adapter="chatterbot.input.TerminalAdapter",
	output_adapter="chatterbot.output.TerminalAdapter",
)

bot.train('chatterbot.corpus.english')
bot.train('chatterbot.corpus.english.greetings')

print("Type something to begin ...")

# The following loop will execute each time the user enters input
while True:
	try:
# We pass None to this method because the parameter
# is not used by the TerminalAdapter
		bot_input = bot.get_response(None)

# Press ctrl-c or ctrl-d on the keyboard to exit
	except (KeyboardInterrupt, EOFError, SystemExit):
		break
