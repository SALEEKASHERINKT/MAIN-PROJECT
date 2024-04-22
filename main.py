from flask import *
from public import public
from admin import admin
from user import user
from company import company

innov=Flask(__name__)
innov.secret_key="key"
innov.register_blueprint(public)
innov.register_blueprint(admin)
innov.register_blueprint(user)
innov.register_blueprint(company)

innov.run(debug=True,port=5607)