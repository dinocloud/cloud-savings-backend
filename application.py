from database import db, create_app
from werkzeug.exceptions import *
from views import *
import os

application = create_app()

@application.errorhandler(401)
@application.errorhandler(404)
@application.errorhandler(403)
@application.errorhandler(400)
@application.errorhandler(500)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e), message=e.description), code

api_prefix = "/api/v1/"

UsersView.register(application, route_prefix=api_prefix)
AwsAccountView.register(application, route_prefix=api_prefix)

if __name__ == '__main__':
    with application.app_context():
        db.create_all()
        application.run(port=os.getenv("APP_PORT", 5000), debug=True)
