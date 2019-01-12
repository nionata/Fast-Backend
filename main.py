from app import app
from flask import jsonify
from flask import flash, request

@app.route('/hello')
def hello():
	try:
		return "Hello World"
	except Exception as e:
		print(e)
	finally:
		print("no")

@app.route('/event', methods=['POST'])
def add_event():
	try:
		_json = request.json
		_name = _json['name']
		resp = jsonify('Event added successfully ' + _name)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		print("nope")

if __name__ == "__main__":
	app.run()
