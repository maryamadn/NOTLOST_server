import os
import psycopg2
from flask import Blueprint, request
from flask_cors import CORS

from Functions.select_photos import select_photos

photos = Blueprint('photos_blueprint', __name__)
CORS(photos)

url = os.environ.get("DATABASE_URI")  # gets variables from environment
connection = psycopg2.connect(url)

#get all items, create item
@photos.route('/', methods=['GET', 'POST'])
def create_photos():
    if request.method == 'POST':
        photo = request.get_json()
        values = list(photo.values())
        with connection:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute("""INSERT INTO photos (url, item_id)
                        VALUES (%s, %s)""", values)
                    except:
                        return {"error": "Validation failed."}, 400

    with connection:
        with connection.cursor() as cursor:
            photos = select_photos(cursor)
        return photos