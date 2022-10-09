def select_photos(cursor, id=''):
    if id == '':
        cursor.execute("SELECT * FROM photos")
    else:
        cursor.execute(f"SELECT * FROM photos WHERE id = {id}")
        
    # get columns of users
    columns = cursor.description
    result = cursor.fetchall()

    # make dict
    photos = []
    for row in result:
        row_dict = {}
        for i, col in enumerate(columns):
            row_dict[col.name] = row[i]
        photos.append(row_dict)
    return photos