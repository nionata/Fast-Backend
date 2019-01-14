import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/api/events')
def get_events():
	try:
		cursor = mysql.connect().cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM events")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)

@app.route('/api/members')
def get_members():
	try:
		cursor = mysql.connect().cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM members")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)

@app.route('/api/types')
def get_types():
	try:
		cursor = mysql.connect().cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM types")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)

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
		if True: #Check inputs
			sql = "INSERT INTO events(event_name, event_type_id, event_start, event_end, event_lat, event_long) VALUES(%s, %s, %s, %s, %s, %s)"
			data = (_name, _type, _start, _end, _lat, _long)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			#run eid thru hash funciton and return the code
			resp = jsonify('Event added successfully')
			resp.status_code = 200
			return resp
	except Exception as e:
		print(e)

@app.route('/api/member', methods=['POST'])
def add_member():
	try:
		_json = request.json
		_first = _json['first name']
		_last = _json['last name']
		if _first and _last:
			sql = "INSERT INTO members(member_first_name, member_last_name) VALUES(%s, %s)"
			data = (_first, _last)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Member added successfully')
			resp.status_code = 200
			return resp
	except Exception as e:
		print(e)

@app.route('/api/signin', methods=['POST'])
def sign_in():
	try:
		_json = request.json
		_code = _json['event code']
		_id = _json['member id']
		if _code and _id:
			#Some sort of hash for code -> eid
			#Go to event
			#Get the type and points associated
			#Add points to member
			#Add attendance to table
			return "ligm"
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
