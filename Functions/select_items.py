from datetime import datetime, timedelta

def select_items(cursor, id='', query='', user_id=''):
    print(query)
    if id == '' and len(query) == 0 and user_id == '':
        cursor.execute("SELECT * FROM items ORDER BY date_time DESC")
    elif id != '':
        cursor.execute(f"SELECT title, category, subcategory, colour, description, items.id, last_location, status, type, date_time, found_lost_by, retrieved_by,json_agg(json_build_object('photo', photos.photo, 'photo_id', photos.id)) AS photos FROM items LEFT JOIN photos ON photos.item_id = items.id WHERE items.id = {id} GROUP BY items.id ORDER BY date_time DESC")
    elif user_id != '':
        cursor.execute(f"SELECT title, category, subcategory, date_time, type, status, items.id, type, json_agg(json_build_object('photo', photos.photo, 'photo_id', photos.id)) AS photos FROM items LEFT JOIN photos ON photos.item_id = items.id WHERE found_lost_by = {user_id} GROUP BY items.id ORDER BY date_time DESC")
    else:
        query_dict = query.to_dict()

        filters = [[k,v] for (k,v) in query_dict.items() if v != '']
        filters_sql = ''
        sort_by = 'DESC'
        search = ''
        from_date = ''
        for pair in filters:
            if pair[0] == 'search':
                search_words = pair[1].split(' ')
                and_or_or = ''
                for word in search_words:
                    search += f"{and_or_or} title ILIKE '%{word}%' OR category::text ILIKE '%{word}%' OR subcategory::text ILIKE '%{word}%' OR colour::text ILIKE '%{word}%' OR description ILIKE '%{word}%'"
                    and_or_or = 'OR'
                search = f'AND ({search})'
            elif pair[0] == 'sort_by':
                sort_by = pair[1]
            elif pair[0] == 'date_range_from':
                from_date = pair[1]
            elif pair[0] == 'date_range_to':
                to_date = datetime.strptime(pair[1], '%Y-%m-%d') + timedelta(days=1)
            else:
                filters_sql += f" AND {pair[0]} = '{pair[1]}'"
        
        # location:

        # date:
        if from_date == '':
            date_range_sql = f"date_time <= '{to_date}'"
        else:
            date_range_sql = f"(date_time BETWEEN '{from_date}' AND '{to_date}')"

        cursor.execute(f"""SELECT category, subcategory, title, date_time, items.id, status, type, array_agg(photos.photo) FROM items LEFT JOIN photos ON photos.item_id = items.id WHERE {date_range_sql} {search}
        {filters_sql} GROUP BY items.id ORDER BY date_time {sort_by}""")
        
    # get columns of items
    columns = cursor.description
    result = cursor.fetchall()

    # make dict
    items = []
    for row in result:
        row_dict = {}
        for i, col in enumerate(columns):
            row_dict[col.name] = row[i]
        items.append(row_dict)
    if len(items) == 0:
        return {"msg": "No items found."}
    else:
        return items




    # cursor.execute("SELECT * FROM items ORDER BY date_time DESC")
    #         # get columns of items
    # columns = cursor.description
    # result = cursor.fetchall()

    # # make dict
    # items = []
    # for row in result:
    #     row_dict = {}
    #     for i, col in enumerate(columns):
    #         row_dict[col.name] = row[i]
    #     items.append(row_dict)
    # if len(items) == 0:
    #     return {"msg": "No items found."}
    # else:
    #     return items