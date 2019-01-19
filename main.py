import pymysql
import time
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request, session
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
			#function to generate a 4 digit code...push to cache
			resp = jsonify('Event added successfully')
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
			#eid = code from cache
			eid = _code
			#Check if member has already signed into event
			if not str(eid) in session:
				#Get the corresponding event
				conn = mysql.connect()
				cursor = conn.cursor(pymysql.cursors.DictCursor)
				cursor.execute("select event_type_id, event_start, event_end, event_lat, event_long from events where event_id=%s" % eid)
				rows = cursor.fetchall()
				if rows:
					row = rows[0]
					#Check if it is within the time range
					curr = time.time()
					if row["event_start"] <= curr and curr <= row["event_end"]:
						#Check location (Add function for proximity)
						if row["event_lat"] == _lat and row["event_long"] == _long:
							cursor.execute("update members set member_points=member_points + (select type_points from types where type_id=%s) where member_id=%s" % (row["event_type_id"], _id))
							cursor.execute("insert into attendance (attendance_event_id, attendance_member_id) values (%s, %s)" % (eid, _id))
							conn.commit()
							resp = "Successfully signed in"
							session[eid] = ""
						else:
							resp = "You are not within the range"
					else:
						resp = "This event is not active"
				else:
					resp = "That is not a valid event code"
			else:
				resp = "You have already signed into this event"
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
