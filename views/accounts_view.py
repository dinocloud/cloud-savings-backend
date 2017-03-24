from flask import jsonify, request, send_file
from flask_classy import FlaskView, route
from model import *
from schemas import *
from utils.validators import *
from utils.authenticators import *


class AwsAccountView(FlaskView):
    route_base = "/accounts/aws"
    awsAccountSchema = AwsAccountSchema()
    awsAccountWithKeysSchema = AwsAccountWithKeysSchema()

    def index(self):
        '''Get all aws accounts'''
        user_string = validate_param(request.args.get('user', None), [(NUMERIC_STRING_VALIDATOR,)])
        user = int(user_string) if user_string is not None else None
        if user is not None:
            validate_access(request.headers.get("Authorization"), [ADMIN_USER, MYSELF_USER], id_myself=user)
            all_accounts = AwsAccount.query.filter(AwsAccount.idUser == user)
        else:
            validate_access(request.headers.get("Authorization"), ADMIN_USER)
            all_accounts = AwsAccount.query
        data = self.awsAccountSchema.dump(all_accounts, many=True).data
        return jsonify({"accounts": data})

    def get(self, id):
        '''Get an aws account'''
        with_keys = validate_param(request.args.get('keys', None), [(VALID_VALUES_VALIDATOR, "true")])
        account = AwsAccount.query.get_or_404(int(id))
        if with_keys is not None:
            validate_access(request.headers.get("Authorization"), ADMIN_USER)
            data = self.awsAccountWithKeysSchema.dump(account).data
        else:
            validate_access(request.headers.get("Authorization"), [ADMIN_USER, MYSELF_USER], id_myself=account.idUser)
            data = self.awsAccountSchema.dump(account).data
        return jsonify(data)

    def post(self):
        '''Insert an aws account'''
        data = request.json
        fancy_name = validate_param(data.get("fancy_name", None), [(TYPE_VALIDATOR, unicode)], required=True)
        access_key = validate_param(data.get("access_key", None), [(TYPE_VALIDATOR, unicode)], required=True)
        secret_key = validate_param(data.get("secret_key", None), [(TYPE_VALIDATOR, unicode)], required=True)
        idUser = validate_param(data.get("user", {}).get("id", None), [(TYPE_VALIDATOR, int)], required=True)
        validate_access(request.headers.get("Authorization"), [ADMIN_USER, MYSELF_USER], id_myself=idUser)
        account = AwsAccount(fancy_name=fancy_name, access_key=access_key, secret_key=secret_key, idUser=idUser)
        db.session.add(account)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify(self.awsAccountSchema.dump(account).data), 201

    def delete(self, id):
        '''Delete an aws account'''
        account = AwsAccount.query.get_or_404(int(id))
        validate_access(request.headers.get("Authorization"), [ADMIN_USER, MYSELF_USER], id_myself=account.idUser)
        db.session.delete(account)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify({"message": "Successfully deleted item.", "id": account.id}), 200

    def put(self, id):
        '''Update an aws account'''
        account = AwsAccount.query.get_or_404(int(id))
        validate_access(request.headers.get("Authorization"), [ADMIN_USER, MYSELF_USER], id_myself=account.idUser)
        data = request.json
        account.fancy_name = validate_param(data.get("fancy_name", None), [(TYPE_VALIDATOR, unicode)], required=True)
        account.access_key = validate_param(data.get("access_key", None), [(TYPE_VALIDATOR, unicode)], required=True)
        account.secret_key = validate_param(data.get("secret_key", None), [(TYPE_VALIDATOR, unicode)], required=True)
        db.session.merge(account)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify({"message": "Successfully updated item.",
                        "item": self.awsAccountSchema.dump(account).data})