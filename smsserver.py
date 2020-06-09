import flask
from flask import *
from flask import Flask
from flaskext.mysql import MySQL
import json
import requests
from google import google

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'app'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'smsweb'
app.config['MYSQL_DATABASE_SOCKET'] = None
mysql.init_app(app)
conn = mysql.connect()
cur = conn.cursor()

def googleSearch(query,phno):
	search_results = google.search(query)
	# print(result.name+"\n"+result.link+"\n"+result.description+"\n\n\n")
	response_string = ''
	response = []
	temp_d = {}
	count = 1
	for result in search_results:
		try:
			response_string += str(count)+" "+result.name.split('›')[0]+"\n"+result.description+"\n\n"
		except:
			pass
		temp_d['slno'] = count
		temp_d['link'] = result.link
		response.append(temp_d)
		count += 1
	response = json.dumps(response)
	# q = "INSERT INTO q_state (Mobile_No,Response) values ('%s','%s')" %(phno,response)
	# cur.execute(q)
	# conn.commit()
	print(response_string)
	return response_string



@app.route('/message', methods = ["GET"])
def receive_sms():
    phno = flask.request.args.get("phoneNumber")[3:]
    msg = flask.request.args.get("message")
    print("Message received from: ",phno)
    print("\nThe Message is:\n",msg)
    res = googleSearch(msg,phno)
    requests.get("http://192.168.1.106:8090/SendSMS?username=salman&password=salman&phone="+phno+"&message="+res)
    return '',200


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug = True)