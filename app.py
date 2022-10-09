from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from Blueprints.users_blueprint import users
from Blueprints.items_blueprint import items
from Blueprints.photos_blueprint import photos
load_dotenv()  # loads variables from .env file into environment

app = Flask(__name__)
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(items, url_prefix='/items')
app.register_blueprint(photos, url_prefix='/photos')

CORS(app)

# secret = 'mary'
# url = os.environ.get("DATABASE_URI")  # gets variables from environment
# connection = psycopg2.connect(url)
                