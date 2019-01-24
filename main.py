import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request, session
from functions import toCode, takeTime

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

@app.route('/api/event/<id>')
def get_event(id):
	try:
		cursor = mysql.connect().cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT attendance_id, attendance_time_in, member_first_name, member_last_name FROM attendance INNER JOIN members ON attendance_member_id=member_id WHERE attendance_event_id=%s" % id)
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

@app.route('/api/member/<id>')
def get_member(id):
	try:
		cursor = mysql.connect().cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT attendance_id, attendance_time_in, event_name, event_start, event_end, type_name FROM attendance inner join events on attendance_event_id=event_id inner join types on event_type_id=type_id where attendance_member_id=%s" % id)
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
		_start = _json['start'] if 'start' in _json else takeTime()
		_end = _json['end']
		_lat = _json['lat']
		_long = _json['long']
		if _name and _type and _start and _end and _lat and _long:
			sql = "INSERT INTO events(event_name, event_type_id, event_start, event_end, event_lat, event_long) VALUES(%s, %s, %s, %s, %s, %s)"
			data = (_name, _type, _start, _end, _lat, _long)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			message = {
				"message": "Event added successfully",
				"code": toCode(_start)
			}
			resp = jsonify(message)
			resp.status_code = 200
			return resp
		else:
			return not_found
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
		else:
			return not_found
	except Exception as e:
		print(e)

@app.route('/api/signin', methods=['POST'])
def sign_in():
	try:
		_json = request.json
		_code = _json['event code']
		_id = _json['member id']
		_lat = _json['lat']
		_long = _json['long']
		if _code and _id and _lat and _long:
			resp = None
			if not str(_code) in session:
				conn = mysql.connect()
				cursor = conn.cursor(pymysql.cursors.DictCursor)
				cursor.execute("SELECT event_id, event_start, event_end, event_lat, event_long, type_points FROM events INNER JOIN types ON event_type_id=type_id WHERE event_start%%10000=%d" % _code)
				rows = cursor.fetchall()
				if rows:
					event = rows[0]
					currTime = takeTime()
					if event["event_start"] <= currTime and currTime <= event["event_end"]:
						if event["event_lat"] == _lat and event["event_long"] == _long: #add proximity
							cursor.execute("SELECT attendance_time_in FROM attendance WHERE attendance_event_id=%d AND attendance_member_id=%d" % (event['event_id'], _id))
							rows = cursor.fetchall()
							if not rows:
								cursor.execute("update members set member_points=member_points+%s where member_id=%s" % (event["type_points"], _id))
								cursor.execute("insert into attendance (attendance_event_id, attendance_member_id, attendance_time_in) values (%d, %d, %d)" % (event['event_id'], _id, currTime))
								conn.commit()
								resp = "Successfully signed in"
								session[str(_code)] = True
							else:
								resp = "You already signed into this event"
						else:
							resp = "You are not within the event range"
					else:
						resp = "This event is not active"
				else:
					resp = "That is not a valid event code"
			else:
				resp = "You already signed into this event"
			resp = jsonify(resp)
			resp.status_code = 200
			return resp
		else:
			return not_found
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
