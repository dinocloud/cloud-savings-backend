from database import db
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    registered = db.Column(db.DateTime(), nullable=False)
    idRole = db.Column(db.Integer, db.ForeignKey('UserRole.id'))
    role = db.relationship("UserRole", foreign_keys=[idRole], cascade="merge")
    idStatus = db.Column(db.Integer, db.ForeignKey('UserStatus.id'))
    status = db.relationship("UserStatus", foreign_keys=[idStatus], cascade="merge")
    devices = db.relationship("Device", uselist=True, backref=db.backref('user_device'),
                               cascade="save-update, merge, delete")
    aws_accounts = db.relationship("AwsAccount", uselist=True, backref=db.backref('user_account'),
                                   cascade="save-update, merge, delete")

    def __init__(self, username=None, password='', email=None, role_id=None, status_id=None, registered=None):
        self.username = username
        self.password = pwd_context.encrypt(password)
        self.email = email
        self.idRole = role_id
        self.idStatus = status_id
        self.registered = registered
        self.devices = []

    def __repr__(self):
        return '<User {0}, {1}>'.format(self.username, self.email)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


class UserRole(db.Model):
    __tablename__ = "UserRole"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, description=None):
        self.description = description

    def __repr__(self):
        return '<User Role {0}>'.format(self.description)


class UserStatus(db.Model):
    __tablename__ = "UserStatus"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, description=None):
        self.description = description

    def __repr__(self):
        return '<User Status {0}>'.format(self.description)


class Device(db.Model):
    __tablename__ = "Device"
    id = db.Column(db.Integer, primary_key=True)
    idRegistration = db.Column(db.String(150), unique=True, nullable=False)
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship("User", foreign_keys=[idUser], cascade="merge")

    def __init__(self, idRegistration=None, idUser=None):
        self.idRegistration = idRegistration
        self.idUser = idUser


class AwsAccount(db.Model):
    __tablename__ = "AwsAccount"
    id = db.Column(db.Integer, primary_key=True)
    access_key = db.Column(db.String(400), unique=True, nullable=False)
    fancy_name = db.Column(db.String(50), unique=True, nullable=False)
    secret_key = db.Column(db.String(400), unique=True, nullable=False)
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship("User", foreign_keys=[idUser], cascade="merge")

    def __init__(self, access_key=None, secret_key=None, fancy_name=None, idUser=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.fancy_name = fancy_name
        self.idUser = idUser