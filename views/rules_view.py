from flask import jsonify, request, send_file
from flask_classy import FlaskView, route
from model import *
from utils.constants import DAYS_CODES, TIME_REGEX, DATETIME_REGEX, EMAIL_REGEX
from schemas import *
from utils.validators import *
from utils.authenticators import *
import datetime


class RuleView(FlaskView):
    route_base = "/rules"
    ruleSchema = RuleSchema()

    def index(self):
        '''Get all rules'''
        account_string = validate_param(request.args.get('aws_account', None), [(NUMERIC_STRING_VALIDATOR,)])
        account = int(account_string) if account_string is not None else None
        user_string = validate_param(request.args.get('user', None), [(NUMERIC_STRING_VALIDATOR,)])
        user = int(user_string) if user_string is not None else None
        if account is not None:
            account_object = AwsAccount.query.get_or_404(account)
            validate_access(request.headers.get("Authorization"), [ADMIN_USER, MYSELF_USER],
                            id_myself=account_object.idUser)
        elif user is not None:
            validate_access(request.headers.get("Authorization"), [ADMIN_USER, MYSELF_USER],
                            id_myself=user)
        else:
            validate_access(request.headers.get("Authorization"), ADMIN_USER)
        all_rules = Rule.query
        all_rules = all_rules.filter(Rule.idAwsAccount == account) if account is not None else all_rules
        all_rules = all_rules.filter(Rule.account.has(AwsAccount.idUser == user)) if user is not None else all_rules
        data = self.ruleSchema.dump(all_rules, many=True).data
        return jsonify({"rules" : data})

    def get(self, id):
        '''Get a rule'''
        rule = Rule.query.get_or_404(int(id))
        validate_access(request.headers.get("Authorization"), [ADMIN_USER, MYSELF_USER], id_myself=rule.awsAccount.idUser)
        data = self.ruleSchema.dump(rule).data
        return jsonify(data)

    def post(self):
        '''Create a new rule'''
        data = request.json
        idAwsAccount = validate_param(data.get("account", {}).get("id", None), [(TYPE_VALIDATOR, int)], required=True)
        aws_account = AwsAccount.query.get_or_404(idAwsAccount)
        validate_access(request.headers.get("Authorization"), [ADMIN_USER, MYSELF_USER],
                        id_myself=aws_account.idUser)
        name = validate_param(data.get("name", None), [(TYPE_VALIDATOR, unicode)], required=True)
        description = validate_param(data.get("description", None), [(TYPE_VALIDATOR, unicode)], required=True)
        idRuleAction = validate_param(data.get("action", {}).get("id", None), [(TYPE_VALIDATOR, int)], required=True)
        idStatus = validate_param(data.get("status", {}).get("id", None), [(TYPE_VALIDATOR, int)], required=True)
        idRuleType = validate_param(data.get("type", {}).get("id", None), [(TYPE_VALIDATOR, int)], required=True)



        filters = []
        for filter in data.get("filters", []):
            filter_key = validate_param(filter.get("key", {}).get("id", None), [(TYPE_VALIDATOR, int)], required=True)
            filter_value = validate_param(filter.get("value", None), [(TYPE_VALIDATOR, unicode)], required=True)
            new_filter = RuleFilter(idKey=filter_key, value=filter_value)
            filters.append(new_filter)

        timestamps = []
        for timestamp in data.get("timestamps", []):
            dayOfWeek = validate_param(timestamp.get("dayOfWeek", None), [(TYPE_VALIDATOR, unicode),
                                                                     (VALID_VALUES_VALIDATOR, DAYS_CODES)])
            if dayOfWeek is not None:
                time = datetime.datetime.strptime(
                validate_param(timestamp.get("timestamp", None), [(REGEX_VALIDATOR, TIME_REGEX)],
                               required=True), "%H:%M")
            else:
                time = datetime.datetime.strptime(
                    validate_param(timestamp.get("timestamp", None), [(REGEX_VALIDATOR, DATETIME_REGEX)],
                                   required=True), "%H:%M")
            new_timestamp = RuleTimestamp(dayOfWeek=dayOfWeek, timestamp=time)
            timestamps.append(new_timestamp)

        rule = Rule(name=name, description=description, idAwsAccount=idAwsAccount, idRuleAction=idRuleAction,
                    idStatus=idStatus, idRuleType=idRuleType, filters=filters, timestamps=timestamps)
        db.session.add(rule)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify(self.ruleSchema.dump(rule).data), 201

    def delete(self, id):
        '''Delete a rule'''
        rule = Rule.query.get_or_404(int(id))
        validate_access(request.headers.get("Authorization"), [ADMIN_USER, MYSELF_USER], id_myself=rule.awsAccount.idUser)
        db.session.delete(rule)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify({"message": "Successfully deleted item.", "id": rule.id}), 200

    def put(self, id):
        '''Update a rule'''
        rule = Rule.query.get_or_404(int(id))
        validate_access(request.headers.get("Authorization"), [ADMIN_USER, MYSELF_USER],
                        id_myself=rule.awsAccount.idUser)
        data = request.json
        rule.name = validate_param(data.get("name", None), [(TYPE_VALIDATOR, unicode)], required=True)
        rule.description = validate_param(data.get("description", None), [(TYPE_VALIDATOR, unicode)], required=True)
        rule.idRuleAction = validate_param(data.get("action", {}).get("id", None), [(TYPE_VALIDATOR, int)], required=True)
        rule.idStatus = validate_param(data.get("status", {}).get("id", None), [(TYPE_VALIDATOR, int)], required=True)
        rule.idRuleType = validate_param(data.get("type", {}).get("id", None), [(TYPE_VALIDATOR, int)], required=True)

        RuleFilter.query.filter(RuleFilter.idRule == int(id)).delete(synchronize_session='evaluate')
        filters = []
        for filter in data.get("filters", []):
            filter_key = validate_param(filter.get("key", {}).get("id", None), [(TYPE_VALIDATOR, int)], required=True)
            filter_value = validate_param(filter.get("value", None), [(TYPE_VALIDATOR, unicode)], required=True)
            new_filter = RuleFilter(idKey=filter_key, value=filter_value)
            filters.append(new_filter)

        RuleTimestamp.query.filter(RuleTimestamp.idRule == int(id)).delete(synchronize_session='evaluate')
        timestamps = []
        for timestamp in data.get("timestamps", []):
            dayOfWeek = validate_param(timestamp.get("dayOfWeek", None), [(TYPE_VALIDATOR, unicode),
                                                                          (VALID_VALUES_VALIDATOR, DAYS_CODES)])
            if dayOfWeek is not None:
                time = datetime.datetime.strptime(
                    validate_param(timestamp.get("timestamp", None), [(REGEX_VALIDATOR, TIME_REGEX)],
                                   required=True), "%H:%M")
            else:
                time = datetime.datetime.strptime(
                    validate_param(timestamp.get("timestamp", None), [(REGEX_VALIDATOR, DATETIME_REGEX)],
                                   required=True), "%H:%M")
            new_timestamp = RuleTimestamp(dayOfWeek=dayOfWeek, timestamp=time)
            timestamps.append(new_timestamp)

        rule.filters = filters
        rule.timestamps = timestamps

        db.session.merge(rule)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return jsonify({"message": "Successfully updated item.",
                        "item": self.ruleSchema.dump(rule).data})
