from werkzeug.exceptions import Unauthorized, Forbidden
from model import *
import base64
from schemas import UserWithPasswordSchema
from passlib.apps import custom_app_context as pwd_context


ADMIN_USER = 1
MYSELF_USER = 2


USER_ROLES = {
    "admin" : 1,
    "consumer" : 2,
    "provider" : 3
}

USER_STATUS = {
    "pending" : 1,
    "ready" : 2,
    "deleted" : 3
}


def decode_username_and_password(basic_auth_string):
    if basic_auth_string is None:
        raise Unauthorized("You should provide user credentials to do this request.")
    data = base64.b64decode(basic_auth_string[6:])
    return [data.split(":")[0], data.split(":")[1]]


def get_user(username, password):
    user = User.query.filter(User.username == str(username)).first()
    userSchema = UserWithPasswordSchema()
    user_dict = userSchema.dump(user, many=False).data
    if len(user_dict) == 0:
        raise Unauthorized("The user %s might not exist." % username)
    if pwd_context.verify(password, str(user_dict.get("password"))):
        raise Unauthorized("The password for user %s is incorrect" % username)
    return user_dict


def validate_admin_user(username, password):
    user_dict = get_user(username, password)
    if user_dict.get("role").get("id") == USER_ROLES.get("admin") \
            and user_dict.get("status").get("id") == USER_STATUS.get("ready"):
        return True
    else:
        return False


def validate_myself_user(username, password, id_myself):
    user_dict = get_user(username, password)
    if int(user_dict.get("id")) != id_myself:
        raise Forbidden("Unable to execute this operation")
    if user_dict.get("status").get("id") == USER_STATUS.get("ready"):
        return True
    else:
        return False


def validate_access(basic_auth_string, access_provided, id_myself=None):
    if not isinstance(access_provided, list):
        access_provided = [access_provided]
    user_and_password = decode_username_and_password(basic_auth_string)
    authenticated = False
    for access in access_provided:
        if not authenticated:
            if access == ADMIN_USER:
                authenticated = validate_admin_user(user_and_password[0], user_and_password[1])
            elif access == MYSELF_USER:
                authenticated = validate_myself_user(user_and_password[0], user_and_password[1], id_myself)
    if not authenticated:
        raise Forbidden("The user %s might not have the right privilegies to execute the request."
                           % user_and_password[0])
