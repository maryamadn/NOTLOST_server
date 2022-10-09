from datetime import datetime, timedelta

def select_items(cursor, id='', query=''):
    if id == '' and query == '':
        cursor.execute("SELECT * FROM items ORDER BY date_time DESC")
    else:
        query_dict = query.to_dict()
        search = query_dict["search"]
        sort_by = query_dict["sort_by"]
        del query_dict["search"]
        del query_dict["sort_by"]
        
        #filters = [[k,v] for (k,v) in query_dict.items()]
        filters = [[k,v] for (k,v) in query_dict.items() if v != '']
        filters_sql = ''
        for pair in filters:
            if pair[0] == 'date_range':
                from_date = pair[1].split(' ')[0]
                to_date = datetime.strptime(pair[1].split(' ')[1], '%Y%m%d') + timedelta(days=1)
                print(from_date, to_date) # must be one day extra so manipulate and plus one....
                # filters_sql += f" AND dates >= '{from_date}' AND dates < '{to_date}'" # depends on front end, need to split 2 dates
            else:
                filters_sql += f" AND {pair[0]} = '{pair[1]}'"
        
        # location: 
        cursor.execute(f"""SELECT * FROM items WHERE (title ILIKE '%{search}%' OR category::text ILIKE '%{search}%' OR subcategory::text ILIKE '%{search}%' OR colour::text ILIKE '%{search}%' OR description ILIKE '%{search}%')
        {filters_sql} ORDER BY date_time {sort_by}""")
        
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