from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
	print(request.args.get("a"))
	return "<h2>Hello World</h2>"