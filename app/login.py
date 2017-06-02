from app import auth, app, db
from .models import Users
from flask import jsonify, g, abort
from datetime import datetime

@auth.verify_password
def verify_password(username_or_token, password):
	#first try to authenticate by token
	user = Users.verify_auth_token(username_or_token)
	if not user:
		#try to authenticate with username and password
		user = Users.query.filter_by(username = username_or_token).first()
		if not user or not user.verify_password(password):
			abort(400)
			return False
	timestamp = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	user.last_login = timestamp
	db.session.commit()
	print (timestamp)
	g.user = user
	print (g.user)
	return True

@app.route('/login')
@auth.login_required
def login():
	id_user = g.user.id_user
	username = g.user.username
	email = g.user.email
	last_login = g.user.last_login
	nama_lengkap = g.user.nama_lengkap
	hp = g.user.hp
	alamat = g.user.alamat
	kode_pos = g.user.kode_pos
	level = g.user.level_user

	if not nama_lengkap:
		nama_lengkap = ""
	if not last_login:
		last_login = ""
	if not alamat:
		alamat = ""
	if not hp:
		hp = ""
	if not kode_pos:
		kode_pos = ""

	return jsonify(
			id_user = str(id_user),
			username = str(username),
			email = str(email),
			last_login = str(last_login),
			nama_lengkap = str(nama_lengkap),
			hp = str(hp),
			alamat = str(alamat),
			kode_pos = str(kode_pos),
			level = str(level)
		)
