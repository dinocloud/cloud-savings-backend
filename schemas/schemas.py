from marshmallow import Schema, fields


class UserRoleSchema(Schema):
    id = fields.Integer()
    description = fields.String()


class UserStatusSchema(Schema):
    id = fields.Integer()
    description = fields.String()


class DeviceSchema(Schema):
    id = fields.Integer()
    idRegistration = fields.String()


class AwsAccountSchema(Schema):
    id = fields.Integer()
    fancy_name = fields.String()


class AwsAccountWithKeysSchema(AwsAccountSchema):
    access_key = fields.String()
    secret_key = fields.String()


class UserWithPasswordSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    password = fields.String()
    email = fields.String()
    registered = fields.DateTime()
    status = fields.Nested(UserStatusSchema())
    role = fields.Nested(UserRoleSchema())


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    registered = fields.DateTime()
    status = fields.Nested(UserStatusSchema())
    role = fields.Nested(UserRoleSchema())


class UserWithAccountsSchema(UserSchema):
    accounts = fields.List(fields.Nested(AwsAccountSchema()))


class UserWithDevicesSchema(UserSchema):
    devices = fields.List(fields.Nested(DeviceSchema()))


class RuleActionSchema(Schema):
    id = fields.Integer()
    description = fields.String()


class RuleStatusSchema(Schema):
    id = fields.Integer()
    description = fields.String()


class RuleTypeSchema(Schema):
    id = fields.Integer()
    description = fields.String()


class RuleFilterKeySchema(Schema):
    id = fields.Integer()
    description = fields.String()


class RuleFilterSchema(Schema):
    id = fields.Integer()
    key = fields.Nested(RuleFilterKeySchema())
    value = fields.String()


class RuleTimestampSchema(Schema):
    id = fields.Integer()
    dayOfWeek = fields.String()
    timestamp = fields.String()


class RuleSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    awsAccount = fields.Nested(AwsAccountSchema())
    action = fields.Nested(RuleActionSchema())
    filters = fields.List(fields.Nested(RuleFilterSchema()))
    status = fields.Nested(RuleStatusSchema())
    type = fields.Nested(RuleTypeSchema())
    timestamps = fields.List(fields.Nested(RuleTimestampSchema()))