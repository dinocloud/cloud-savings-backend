from flask import jsonify, request, send_file
from flask_classy import FlaskView, route
from model import *
from schemas import *
from utils.constants import ID_ADMIN_ROLE
from utils.validators import *
from utils.authenticators import *
from passlib.apps import custom_app_context as pwd_context
import datetime


class UsersView(FlaskView):
    route_base = "/users/"
    userSchema = UserSchema()
    userRoleSchema = UserRoleSchema()
    userWithDevicesSchema = UserWithDevicesSchema()
    EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    def index(self):
        '''Get all users'''
        validate_access(request.headers.get("Authorization"), ADMIN_USER)
        all_users = User.query.order_by(User.username.desc())
        data = self.userSchema.dump(all_users, many=True).data
        return jsonify({"users" : data})

    def get(self, id):
        '''Get an user'''
        validate_access(request.headers.get("Authorization"), ADMIN_USER)
        user = User.query.get_or_404(int(id))
        return jsonify(self.userSchema.dump(user).data)

    def post(self):
        '''Insert an user'''
        validate_access(request.headers.get("Authorization"), ADMIN_USER)
        data = request.json
        username = validate_param(data.get("username", None), [(TYPE_VALIDATOR, unicode)])
        password = validate_param(data.get("password", None), [(TYPE_VALIDATOR, unicode)])
        email = validate_param(data.get("email", None), [(TYPE_VALIDATOR, unicode), (REGEX_VALIDATOR, self.EMAIL_REGEX)])
        role = validate_param(data.get("role", {}).get("id", None), [(TYPE_VALIDATOR, int)])
        status = validate_param(data.get("status", {}).get("id", None), [(TYPE_VALIDATOR, int)])
        user = User(username=username, password=password, email=email, role_id=role, status_id=status,
                    registered=datetime.datetime.now())
        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify(self.userSchema.dump(user).data), 201

    def delete(self, id):
        '''Delete an user'''
        validate_access(request.headers.get("Authorization"), ADMIN_USER)
        user = User.query.get_or_404(int(id))
        db.session.delete(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify({"message" : "Successfully deleted item.", "id" : user.id}), 200

    def put(self, id):
        '''Update an user'''
        validate_access(request.headers.get("Authorization"), ADMIN_USER)
        user = User.query.get_or_404(int(id))
        data = request.json
        user.username = validate_param(data.get("username", None), [(TYPE_VALIDATOR, unicode)])
        user.password = pwd_context.encrypt(validate_param(data.get("password", None), [(TYPE_VALIDATOR, unicode)]))
        user.email = validate_param(data.get("email", None), [(TYPE_VALIDATOR, unicode), (REGEX_VALIDATOR,
                                                                                      self.EMAIL_REGEX)])
        user.role = UserRole.query.get_or_404(validate_param(data.get("role", {}).get("id", None), [(TYPE_VALIDATOR, int)]))
        user.status = UserStatus.query.get_or_404(validate_param(
            data.get("status", {}).get("id", None), [(TYPE_VALIDATOR, int)]))
        db.session.merge(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify({"message": "Successfully updated item.",
                        "item": self.userSchema.dump(user).data})

    def login(self):
        id_role_string = validate_param(request.args.get("role", None), [(NUMERIC_STRING_VALIDATOR,)], required=True)
        id_role = int(id_role_string)
        if id_role == ID_ADMIN_ROLE:
            validate_access(request.headers.get("Authorization"), ADMIN_USER)
        else:
            raise BadRequest("The role might not be valid.")
        return jsonify({"message" : "Login successful"}), 200

    def checkusername(self):
        username = request.args.get('username')
        user = User.query.filter(User.username==str(username))
        user_dict = self.userSchema.dump(user, many=True).data
        if len(user_dict) == 0:
            return jsonify({"message" : "Username available"}), 200
        else:
            return jsonify({"message": "Username already exists"}), 409

    def checkemail(self):
        email = request.args.get('email')
        user = User.query.filter(User.email==str(email))
        user_dict = self.userSchema.dump(user, many=True).data
        if len(user_dict) == 0:
            return jsonify({"message" : "Email available"}), 200
        else:
            return jsonify({"message": "Email already exists"}), 409