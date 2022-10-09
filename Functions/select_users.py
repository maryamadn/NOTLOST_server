def select_users(cursor, id='', username=''):
    if id == '' and username == '':
        cursor.execute("SELECT * FROM users")
    elif id == '':
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    else:
        cursor.execute(f"SELECT * FROM users WHERE id = {id}")
        
    # get columns of users
    columns = cursor.description
    result = cursor.fetchall()

    # make dict
    users = []
    for row in result:
        row_dict = {}
        for i, col in enumerate(columns):
            row_dict[col.name] = row[i]
        users.append(row_dict)
    return users