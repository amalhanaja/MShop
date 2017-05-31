from app import db, app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer 
	as Serializer, BadSignature, SignatureExpired)

class Users(db.Model):
	id_user = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True)
	email = db.Column(db.String, unique=True)
	last_login = db.Column(db.String)
	user_password = db.Column(db.String)
	level_user = db.Column(db.String(20), default="USER")
	nama_lengkap = db.Column(db.String)
	hp = db.Column(db.String(16))
	alamat = db.Column(db.String)
	kode_pos = db.Column(db.String(5))



	def __repr__(self):
		return '<User %r>' % self.id_user

	def hash_password(self, password):
		self.user_password = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.user_password)

	def generate_auth_token(self, expiration=600):
		s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
		return s.dumps({"id_user": self.id_user})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
			print (data)
		except SignatureExpired:
			return None
		except BadSignature:
			return None

		user = Users.query.get(data['id_user'])
		return user