from flask import Flask, request, render_template
import base64
import json

app = Flask(__name__)

@app.route("/")
def index():
	client_id = "feaf6ca63ed66d5306996f8a3acc58a2"
	return render_template("signup.html", client_id=client_id, scope="open_id", response_type="id_token")

@app.route("/callback/")
def callback():
	id_token = request.args.get("id_token")
	payload = id_token.split('.')[1]
	print(payload)
	data = base64.b64decode(payload + "==").decode("utf-8")
	payload_data = json.loads(data)
	email  = payload_data['email']
	username = payload_data['username']
	return render_template("callback.html", username=username, email=email)