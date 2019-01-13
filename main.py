import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/api/event', methods=['POST'])
def add_event():
	try:
		_json = request.json
		_name = _json['name']
		_type = _json['type']
		_start = _json['start']
		_end = _json['end']
		_lat = _json['lat']
		_long = _json['long']
		if True: #Add some logic
			sql = "INSERT INTO events(event_name, event_type_id, event_start, event_end, event_lat, event_long) VALUES(%s, %s, %s, %s, %s, %s)"
			data = (_name, _type, _start, _end, _lat, _long)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Event added successfully')
			resp.status_code = 200
			return resp
	except Exception as e:
		print(e)

@app.errorhandler(404)
def not_found(error=None):
	message = {
		'status': 404,
		'message': 'Not Found: ' + request.url,
	}
	resp = jsonify(message)
	resp.status_code = 404
	return resp

if __name__ == "__main__":
	app.run()
