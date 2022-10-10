import os
import psycopg2
from flask import Blueprint, request
from flask_cors import CORS
import bcrypt
import jwt

from Functions.select_users import select_users

users = Blueprint('users_blueprint', __name__)
CORS(users)

secret = os.environ.get("SECRET")
url = os.environ.get("DATABASE_URI")  # gets variables from environment
connection = psycopg2.connect(url)

#get all users, create user
@users.route('/', methods=['GET', 'POST'])
def get_create_users():
    if request.method == 'POST':
        user = request.get_json()
        #add is_admin value
        user["is_admin"] = False
        #hash password
        password = user["password"]
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(bytes, salt).decode('utf-8')
        user["password"] = hashed_password

        #create list of user values
        values = list(user.values())
        with connection:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute("""INSERT INTO users (username, password, email, full_name, phone, is_admin)
                        VALUES (%s, %s, %s, %s, %s, %s)""", values)
                    except Exception as error:
                        print('ni', error)
                        return {"error": f'{error}'}, 400

    with connection:
        with connection.cursor() as cursor:
            users = select_users(cursor)

        return users

#get one user, delete one user, edit one user
@users.route('/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def user(id):
    if request.method == 'DELETE':
        with connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT FROM users WHERE id={id}")
                    check_exist = cursor.fetchall()
                    print(check_exist)
                    if len(check_exist) == 0:
                        return {"error": "User not found."}, 404
                    else:
                        cursor.execute(f"DELETE FROM users WHERE id={id}")
                        return {"msg": "Successfully deleted user."}, 200

    elif request.method == 'PUT':
        user = request.get_json()
        if user["password"] == '':
            del user["password"]
        else:
            password = user["password"]
            bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(bytes, salt).decode('utf-8')
            user["password"] = hashed_password
        values = list(user.values())
        values.append(id)
        with connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(f"SELECT FROM users WHERE id={id}")
                    check_exist = cursor.fetchall()
                    if len(check_exist) == 0:
                        return {"error": "User not found."}, 404
                    elif "password" in user:
                        cursor.execute("UPDATE users SET username=%s, password=%s, email=%s, full_name=%s, phone=%s, is_admin=%s WHERE id=%s", values)
                    else:
                        cursor.execute("UPDATE users SET username=%s, email=%s, full_name=%s, phone=%s, is_admin=%s WHERE id=%s", values)
                except:
                    return {"error": "Validation failed."}, 400

    with connection:
        with connection.cursor() as cursor:
            user = select_users(cursor, id)
            if len(user) == 0:
                return {"error": "User not found."}, 404

        return user[0], 200

# login
@users.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data["username"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
            check_exist = cursor.fetchall()
            print(check_exist)
            if len(check_exist) == 0:
                return {"error": "Validation failed."}, 401
            else:
                password = check_exist[0][2].encode('utf-8')
                input_password = data["password"].encode('utf-8')
                check_password = bcrypt.checkpw(input_password, password)
                if check_password == False:
                    return {"error": "Validation failed."}, 401
                else:
                    payload = select_users(cursor, username=username)[0]
                    del payload["password"]
                    token = jwt.encode(payload, secret)
                    return {"msg": "Successful sign in.", "token": token}, 200