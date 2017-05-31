from app import app, auth
from flask import jsonify, g
from .models import Users

@auth.verify_password
def verify_password(username_or_token, password):
	#try to authenticate with username and password
	user = Users.query.filter_by(username = username_or_token).first()
	if not user or not user.verify_password(password):
		return False
	g.user = user
	return True

@app.route('/get_token')
@auth.login_required
def get_token():
	token = g.user.generate_auth_token(600)
	return jsonify(token = token.decode('ASCII'))