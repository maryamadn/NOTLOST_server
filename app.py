import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, Blueprint
from flask_cors import CORS
# from example_blueprint import example_blueprint

load_dotenv()  # loads variables from .env file into environment

app = Flask(__name__)

# app.register_blueprint(example_blueprint, url_prefix='/blueprint')
CORS(app)

url = os.environ.get("DATABASE_URI")  # gets variables from environment
connection = psycopg2.connect(url)

@app.route('/users', methods=['GET'])
def users():
    with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                
                # get columns of users
                columns = list(cursor.description)
                result = cursor.fetchall()

                # make dict
                users = []
                for row in result:
                    row_dict = {}
                    for i, col in enumerate(columns):
                        row_dict[col.name] = row[i]
                    users.append(row_dict)
            return users