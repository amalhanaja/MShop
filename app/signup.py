from flask import request, jsonify, abort, g
from app import app, db, auth
from .models import Users

@app.route('/signup', methods=['POST'])
def sign_up():
	username = request.form.get('username')
	password = request.form.get('password')
	email = request.form.get('email')
	if not username or not password or not email:
		abort(400)
	if Users.query.filter_by(username = username).first() is not None :
		abort(400)
	if Users.query.filter_by(email = email).first() is not None :
		abort(400)
	user = Users(
			username = username,
			email = email
		)
	user.hash_password(password)
	db.session.add(user)
	db.session.commit()
	return jsonify(
			message="Anda Baru saja terdaftar"
		)

@app.route('/create_user/<level>', methods=['POST'])
def create_user(level):
	username = request.form.get('username')
	password = request.form.get('password')
	email = request.form.get('email')
	full_name = request.form.get('full_name')
	level = level.upper()

	if not username or not password or not email or not full_name:
		abort(400)
	if Users.query.filter_by(username = username).first() is not None :
		abort(400)
	if Users.query.filter_by(email = email).first() is not None :
		abort(400)

	if level == 'ADMIN' or level == 'OPERATOR':
		user = Users(
				username = username,
				email = email,
				full_name = full_name,
				level_user = level
			)
		user.hash_password(password)
		db.session.add(user)
		db.session.commit()
		return jsonify(
				message="Anda Baru saja terdaftar sebagai " + level.upper()
		)
	else:
		abort(400)