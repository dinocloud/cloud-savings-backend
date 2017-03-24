from database import db


class Rule(db.Model):
    __tablename__ = "Rule"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200))
    idAwsAccount = db.Column(db.Integer, db.ForeignKey('AwsAccount.id'))
    awsAccount = db.relationship("AwsAccount", foreign_keys=[idAwsAccount], cascade="merge")
    idRuleAction = db.Column(db.Integer, db.ForeignKey('RuleAction.id'))
    action = db.relationship("RuleAction", foreign_keys=[idRuleAction], cascade="merge")
    filters = db.relationship("RuleFilter", uselist=True, backref=db.backref('rule_rule_filter'),
                                   cascade="save-update, merge, delete")
    idStatus = db.Column(db.Integer, db.ForeignKey('RuleStatus.id'))
    status = db.relationship("RuleStatus", foreign_keys=[idStatus], cascade="merge")
    idRuleType = db.Column(db.Integer, db.ForeignKey('RuleType.id'))
    type = db.relationship("RuleType", foreign_keys=[idRuleType], cascade="merge")
    timestamps = db.relationship("RuleTimestamp", uselist=True, backref=db.backref('rule_rule_timestamp'),
                                   cascade="save-update, merge, delete")

    def __init__(self, name=None, description=None, idAwsAccount=None, idRuleAction=None, idStatus=None,
                 idRuleType=None, filters=None, timestamps=None):
        self.name = name
        self.description = description
        self.idAwsAccount = idAwsAccount
        self.idRuleAction = idRuleAction
        self.idStatus = idStatus
        self.idRuleType = idRuleType
        self.filters = filters
        self.timestamps = timestamps


class RuleAction(db.Model):
    __tablename__ = "RuleAction"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, description=None):
        self.description = description


class RuleFilter(db.Model):
    __tablename__ = "RuleFilter"
    id = db.Column(db.Integer, primary_key=True)
    idKey = db.Column(db.Integer, db.ForeignKey('RuleFilterKey.id'))
    key = db.relationship("RuleFilterKey", foreign_keys=[idKey], cascade="merge")
    value = db.Column(db.String(20), nullable=False)
    idRule = db.Column(db.Integer, db.ForeignKey('Rule.id'))
    rule = db.relationship("Rule", foreign_keys=[idRule], cascade="merge, delete")

    def __init__(self, idKey=None, value=None):
        self.idKey = idKey
        self.value = value


class RuleFilterKey(db.Model):
    __tablename__ = "RuleFilterKey"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, description=None):
        self.description = description


class RuleStatus(db.Model):
    __tablename__ = "RuleStatus"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, description=None):
        self.description = description


class RuleTimestamp(db.Model):
    __tablename__ = "RuleTimestamp"
    id = db.Column(db.Integer, primary_key=True)
    dayOfWeek = db.Column(db.String(2))
    timestamp = db.Column(db.String(20), nullable=False)
    idRule = db.Column(db.Integer, db.ForeignKey('Rule.id'))
    rule = db.relationship("Rule", foreign_keys=[idRule], cascade="merge, delete")

    def __init__(self, dayOfWeek=None, timestamp=None):
        self.dayOfWeek = dayOfWeek
        self.timestamp = timestamp


class RuleType(db.Model):
    __tablename__ = "RuleType"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, description=None):
        self.description = description