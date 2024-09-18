from flask import Flask
from backend.models import *
from backend.apicontrollers import api
from sqlalchemy import func




app=Flask(__name__)
app.secret_key = 'dhfbwkihlqw;qn7@'
app.debug=True
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///SICs.sqlite3"

db.init_app(app)
api.init_app(app)
app.app_context().push()

from backend.controllers import *


if __name__=="__main__":
    app.run()
