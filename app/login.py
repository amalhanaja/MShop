from app import auth, app, db
from .models import Users
from flask import jsonify, g
from datetime import datetime

@auth.verify_password
def verify_password(username_or_token, password):
	#first try to authenticate by token
	user = Users.verify_auth_token(username_or_token)
	if not user:
		#try to authenticate with username and password
		user = Users.query.filter_by(username = username_or_token).first()
		if not user or not user.verify_password(password):
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
	return jsonify(
			id_user = g.user.id_user,
			username = g.user.username,
			email = g.user.email,
			last_login = g.user.last_login,
			nama_lengkap = g.user.nama_lengkap,
			hp = g.user.hp,
			alamat = g.user.alamat,
			kode_pos = g.user.kode_pos,
			level = g.user.level_user
		)
