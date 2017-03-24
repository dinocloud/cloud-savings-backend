import os
class DBSettings:
    DB_ENGINE = "mysql+pymysql"
    DB_HOST = os.getenv("RDS_HOSTNAME","cloudsavings.cwzu3zdkispx.sa-east-1.rds.amazonaws.com:3306")
    DB_NAME = os.getenv("RDS_DB_NAME","cloudsavings")
    DB_PORT = os.getenv("RDS_PORT","3306")
    DB_USER = os.getenv("RDS_USERNAME","root")
    DB_PASSWORD = os.getenv("RDS_PASSWORD","")
    SQLALCHEMY_DATABASE_URI = "{0}://{1}:{2}@{3}/{4}".format(DB_ENGINE, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)