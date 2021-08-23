import pymysql
import geopy.distance
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request, session
from functions import generateCode, takeTime, getTimeout
from cache import cache

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
		cursor.execute("SELECT attendance_id, attendance_time_in, event_name, event_start, event_end FROM attendance inner join events on attendance_event_id=event_id")
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

@app.route('/api/cache')
def get_cache():
	return goodResp(cache)

@app.route('/api/session')
def get_session():
	thisSession = {}
	for key in session:
		thisSession[key] = session[key]
	return goodResp(thisSession)

@app.route('/api/clearsession')
def clear_session():
	session.clear()
	return goodResp("Session successfully cleared")

@app.route('/api/event', methods=['POST'])
def add_event():
	try:
		_json = request.json
		_name = _json['name']
		_start = _json['start'] if 'start' in _json else takeTime()
		_end = _json['end']
		_lat = _json['lat']
		_long = _json['long']
		if _name and _start and _end and _lat and _long:
			sql = "INSERT INTO events(event_name, event_start, event_end, event_lat, event_long) VALUES(%s, %s, %s, %s, %s)"
			data = (_name, _start, _end, _lat, _long)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			code = generateCode(cache.get_dict().keys())
			cache.set(code, cursor.lastrowid, timeout=getTimeout(_end))
			message = {
				"message": "Event added successfully",
				"code": code
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
		
		if not (_code and _id and _lat and _long):
			return not_found
		
		eventId = cache.get(_code)
		
		if not eventId:
			return goodResp("This is not a valid event code")
		
		if str(eventId) in session:
			return goodResp("You already signed into this event")
		
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT event_start, event_end, event_lat, event_long FROM events WHERE event_id=%d" % eventId)
		rows = cursor.fetchall()

		if not rows:
			return goodResp("That is not a valid event code")
		
		event = rows[0]
		currTime = takeTime()

		if not (event["event_start"] <= currTime and currTime <= event["event_end"]):
			return goodResp("This event is not active")
				
		userCoords = (_lat, _long)
		eventCoords = (event["event_lat"], event["event_long"])
		dist = geopy.distance.vincenty(userCoords, eventCoords).miles
		if not (dist <= 0.068):
			return goodResp("You are not within the event range")
				
		cursor.execute("SELECT attendance_time_in FROM attendance WHERE attendance_event_id=%d AND attendance_member_id=%d" % (eventId, _id))
		rows = cursor.fetchall()

		if rows:
			return goodResp("You already signed into this event")

		cursor.execute("insert into attendance (attendance_event_id, attendance_member_id, attendance_time_in) values (%d, %d, %d)" % (eventId, _id, currTime))
		conn.commit()
		session[str(eventId)] = True
		return goodResp("Successfully signed in")
	except Exception as e:
		print(e)

def goodResp(message):
	resp = jsonify(message)
	resp.status_code = 200
	return resp

@app.errorhandler(404)
def not_found(error=None):
	message = {
		'status': 404,
		'message': 'Not Found: ' + request.url,
	}
	resp = jsonify(message)
	resp.status_code = 404
	return resp

@app.after_request
def add_header(resp):
	resp.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
	resp.headers.add('Access-Control-Allow-Credentials', 'true')
	resp.headers.add('Access-Control-Allow-Methods', 'GET,HEAD,OPTIONS,POST,PUT')
	resp.headers.add('Access-Control-Allow-Headers', 'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers')
	return resp

if __name__ == "__main__":
	app.run()
