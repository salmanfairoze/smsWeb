import flask
from flask import *
from flask import Flask
from flaskext.mysql import MySQL
import json
import requests
from Google.google import google
import wolframalpha
from nearest_hospitals import *

# mysql = MySQL()
app = Flask(__name__)

# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'app'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
# app.config['MYSQL_DATABASE_DB'] = 'smsweb'
# app.config['MYSQL_DATABASE_SOCKET'] = None
# mysql.init_app(app)
# conn = mysql.connect()
# cur = conn.cursor()
avoid_rep = [0]
def googleSearch(query,phno):
	client = wolframalpha.Client("E53W7Y-3XKP3G7GP8")
	res = client.query(query)
	try:
		answer = next(res.results).text
		print(next(res.results).text)
		if answer != "":
			return answer
			# requests.get("http://192.168.1.107:8090/SendSMS?username=salman&password=salman&phone="+phno+"&message="+answer)
	except Exception as e:
		print("Exception occured")
		print(e)
	search_results = google.search(query)
	# print(result.name+"\n"+result.link+"\n"+result.description+"\n\n\n")
	response_string = ''
	response = []
	temp_d = {}
	count = 1
	for result in search_results:
		if count > 3:
			break
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
	print("\nreponse is:\n",response_string)
	return response_string



@app.route('/message', methods = ["GET"])
def receive_sms():
	avoid_rep[0]+=1
	if avoid_rep[0]%2 == 0:
		return 'Repeated Query',400
	phno = flask.request.args.get("phoneNumber")[3:]
	m_msg = flask.request.args.get("message")
	if ("query" not in m_msg) and ("hi" not in m_msg):
		return '',400
	print("\nMessage received from: ",phno)
	print("The Message is: ",m_msg,"\n")
	try:
		msg = m_msg.split(":") # query:begin diagnosis
	except:
		pass
	# res = googleSearch(msg,phno)

	# Welcome
	if "hi" == m_msg:
		print(m_msg)
		welcome_1 = "1. 'query:begin diagnosis' to take a COVID-19 Diagnosis Test\n"
		welcome_2 = "2. 'query:hospitals:Your Area Name' to find hospitals in your area\n"
		welcome_3 = "3. 'query:zones:district name' to get the zone information of the district\n"
		welcome_4 = "4. 'query:stats:district/state name' to get its COVID-19 Stats\n"
		welcome_5 = "5. 'query:chat:your question' to get other medical COVID-19 related advice\n"
		resp = "Reply with:\n"+welcome_1+welcome_2+welcome_3+welcome_4+welcome_5
		# requests.get("http://192.168.1.102:8090/SendSMS?username=salman&password=salman&phone="+phno+"&message="+resp)
		print(resp)

	# Diagnosis
	elif "begin diagnosis" in msg[1]:
		resp = requests.post("http://192.168.1.104:5050/diagnosis",json={"user_response":"begin diagnosis"})
		# requests.get("http://192.168.1.102:8090/SendSMS?username=salman&password=salman&phone="+phno+"&message="+resp.text)
		print(resp.text)
	
	# Answers to Diagnosis
	elif "answer" in msg[1]:
		resp = requests.post("http://192.168.1.104:5050/diagnosis",json={"user_response":msg[2]})
		# requests.get("http://192.168.1.102:8090/SendSMS?username=salman&password=salman&phone="+phno+"&message="+resp.text)
		print(resp.text)

	# Chat with bot	
	elif "chat" in msg[1]:
		resp = requests.post("http://192.168.1.104:5050/chat",json={"user_response":msg[2]})
		# requests.get("http://192.168.1.102:8090/SendSMS?username=salman&password=salman&phone="+phno+"&message="+resp.text)
		print(resp.text)

	# Nearest Hospitals
	elif "hospitals" in msg[1]: # query:hospitals:area name
		areaname = msg[2]
		query_string = "Hospitals Near " + areaname
		resp = location(query_string)
		# requests.get("http://192.168.1.102:8090/SendSMS?username=salman&password=salman&phone="+phno+"&message="+resp)
		print(resp)

	# Zone Query # query:zone:district name
	elif "zone" in msg[1] or "stats" in msg[1]:
		dname = msg[2]
		# res = call()
		"""
		zone type (red etc)
		district stats:
			-
			-
			-
		percentage of active cases in your district <%>
		state stats:
			-
			-
			-
		"""
		return res

	# Corona Stats
	# elif "stats" in msg[1]: # query:stats:state:name query:stats:district:name
	# 	name = msg[2]

	else:
		pass
	return '',200


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug = True)
