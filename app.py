import os
from flask import Flask
from flask_restful import Api
from db import db


app =Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = os.environ.get("app_secret_key", "daskldsaf#@%$#@$cc")

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    db.init_app(app)
    app.run()