import os
import psycopg2
from flask import Blueprint, request
from flask_cors import CORS

from Functions.select_photos import select_photos

photos = Blueprint('photos_blueprint', __name__)
# cors = CORS(photos, resources={r'*': {'origins': 'http://localhost:3000'}})

url = os.environ.get("DATABASE_URI")  # gets variables from environment
connection = psycopg2.connect(url)

#get all photos, create photo
@photos.route('/', methods=['GET', 'POST'])
def create_photos():
    if request.method == 'POST':
        body = request.get_json()
        photo = body["photo"]
        item_id = body["item_id"]

        with connection:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute(f"""INSERT INTO photos (photo, item_id)
                            VALUES ('{photo}', {item_id})""")
                        
                    except Exception as error:
                        print(error)
                        return {"error": "Validation failed."}, 400
                        
    with connection:
        with connection.cursor() as cursor:
            photos = select_photos(cursor)
        return photos

#delete photos of one item
@photos.route('/byitem/<int:id>', methods=['GET', 'DELETE'])
def delete_photos(id):
    if request.method == 'DELETE':
        with connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT photos.id FROM photos WHERE item_id={id}")
                    check_exist = cursor.fetchall()
                    print(check_exist)
                    if len(check_exist) == 0:
                        return {"error": "Photo not found."}, 404
                    else:
                        cursor.execute(f"DELETE FROM photos WHERE item_id={id}")
                        return {"msg": "Successfully deleted photos of item."}, 200

    with connection:
        with connection.cursor() as cursor:
            photos = select_photos(cursor, id)
            if len(photos) == 0:
                return {"error": "Photos of item not found."}, 404

        return photos[0], 200

#delete one photo
@photos.route('/<int:id>', methods=['GET', 'DELETE'])
def delete_photo(id):
    if request.method == 'DELETE':
        try:
            with connection:
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT FROM photos WHERE id={id}")
                        check_exist = cursor.fetchall()
                        if len(check_exist) == 0:
                            return {"error": "Photo not found."}, 404
                        else:
                            cursor.execute(f"DELETE FROM photos WHERE id={id}")
                            return {"msg": "Successfully deleted photo."}, 200
        except Exception as error:
            print(error)
            return {"error": "Unable to delete photo"}, 400

    # with connection:
    #     with connection.cursor() as cursor:
    #         photo = select_photos(cursor, id)
    #         if len(photo) == 0:
    #             return {"error": "Photo not found."}, 404

    #     return photo[0], 200