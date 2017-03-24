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


class AwsAccountWithKeysSchema(Schema):
    id = fields.Integer()
    fancy_name = fields.String()
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


class UserWithAccountsSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    registered = fields.DateTime()
    status = fields.Nested(UserStatusSchema())
    role = fields.Nested(UserRoleSchema())
    accounts = fields.List(fields.Nested(AwsAccountSchema()))


class UserWithDevicesSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    registered = fields.DateTime()
    status = fields.Nested(UserStatusSchema())
    role = fields.Nested(UserRoleSchema())
    devices = fields.List(fields.Nested(DeviceSchema()))


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    registered = fields.DateTime()
    status = fields.Nested(UserStatusSchema())
    role = fields.Nested(UserRoleSchema())