from flask import Flask


app = Flask(__name__, static_url_path="/static", static_folder="static")
app.secret_key = ''

from app import views