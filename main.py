from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/api/event', methods=['POST'])
def add_event():
	try:
		_json = request.json
		print(_json)
		_name = _json['name']
		_type = _json['type']
		_start = _start['start']
		_end = _end['end']
		_lat = _lat['lat']
		_long = _long['long']
		resp = jsonify('Event added successfully ' + _name)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		print("nope")

if __name__ == "__main__":
	app.run()
