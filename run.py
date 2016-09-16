from app import app, db

application = app
application.run(debug=True)


# import os
# from app import create_app, db
# from flask.ext.script import Manager, Shell

# application = create_app(os.getenv('FLASK_CONFIG') or 'default')
# manager = Manager(application)