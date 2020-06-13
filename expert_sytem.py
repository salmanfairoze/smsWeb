from chatterbot import ChatBot
from chatterbot import comparisons
from chatterbot import response_selection
from chatterbot import filters
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

from flask import Flask, request, jsonify
#creating a dfa bot

class DiagBot:

    def __init__(self):
        self.str1 = "Do you have fever along with symptoms of acute respiratory illness ? like cough or shortness of breath?"
        self.str2 = "Did you travel to any area/country or territory reporting local transmission of covid-19 disease within the past 17 days ?"
        self.str3 = "Did you come into contact with a possible covid-19 carrier ?"
        self.str4 = "Reply with query:answers:yes/no yes/no yes/no"
        self.str5 = "To know if you have travelled to a COVID-19 Hotspot (Red Zone) reply with 'query:zone:district name'" 
        self.str6 = self.str1+'\n'+self.str2+'\n'+self.str3+'\n'+self.str4 +'\n'+self.str5+'\n'

    def get_response(self, text):

        if(text == 'begin diagnosis'):

            return self.str6

        else:

            response = text.split(' ')

            for i in range(len(response)):

                response[i] = response[i].strip('\n').strip(" ").lower()

            if(response[0] == 'yes' and response[1] == 'yes' and response[2] == 'yes'):

                return "Reach the nearest COVID-19 testing center immediately, you have a high risk of being infected\nTo know Nearest Hospitals reply with query:hospitals:area_name"

            elif(response[0] == 'yes' and response[1] == 'yes' and response[2] == 'no'):

                return "Reach the nearest COVID-19 testing center immediately, you have a high risk of being infected\nTo know Nearest Hospitals reply with query:hospitals:area_name"

            elif(response[0] == 'yes' and response[1] == 'no' and response[2] == 'yes'):

                return "Reach the nearest COVID-19 testing center immediately, you have a high risk of being infected\nTo know Nearest Hospitals reply with query:hospitals:area_name"

            elif(response[0] == 'yes' and response[1] == 'no' and response[2] == 'no'):

                return "Seek medical attention and self quarantine is strictly advised.\nTo know Nearest Hospitals reply with query:hospitals:area_name"

            elif(response[0] == 'no' and response[1] == 'yes' and response[2] == 'yes'):

                return "Self quarantine is strictly advised"

            elif(response[0] == 'no' and response[1] == 'yes' and response[2] == 'no'):

                return "Self quarantine is strictly advised"

            elif(response[0] == 'no' and response[1] == 'no' and response[2] == 'yes'):

                return "Self quarantine is strictly advised"

            elif(response[0] == 'no' and response[1] == 'no' and response[2] == 'no'):

                return "You are less likely to be infected with COVID-19. However, take precautions:\nMaintain Social Distancing\nAvoid Crowd Gathering\nAvoid Travelling to COVID Hotspots\nWash Your Hands Frequently\nStay Home, Stay Safe!!"

# Creating ChatBot Instance
chatbot1 = ChatBot(
    'CoronaBot1',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand. I am still learning.',
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri = 'sqlite:///database.sqlite3'
)

chatbot2 = DiagBot()

app = Flask(__name__)

@app.route('/train', methods = ["HEAD"])
def train_bots():

    # Training with English Corpus Data
    trainer_corpus = ChatterBotCorpusTrainer(chatbot1)
    trainer_corpus.train(
        "chatterbot.corpus.english"
    )

    training_data_corona_ques = open('training_data/corona_ques_corpus.txt').read().splitlines()
    training_data_personal_ques = open('training_data/personal_ques.txt').read().splitlines()
    training_data = training_data_personal_ques + training_data_corona_ques

    trainer = ListTrainer(chatbot1)
    trainer.train(training_data)

    return "",200


@app.route('/diagnosis', methods = ["POST"])
def diagbot():

    user_req = request.get_json()
    return str(chatbot2.get_response(user_req['user_response']))

@app.route('/chat', methods = ["POST"])
def chatbot():

    user_req = request.get_json()
    return str(chatbot1.get_response(user_req['user_response']))


if(__name__ == '__main__'):
    app.run(host= '0.0.0.0',debug = True, port = 5050)
