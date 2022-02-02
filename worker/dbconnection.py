import mysql.connector
def getSqlConnection():
    config = {
        "user": "root",
        "host": "db",
        "port": "3306",
        "password": "pass",
        "database": "mytest",
        "auth_plugin": "mysql_native_password",
    }
    connection = mysql.connector.connect(**config)
    return connection


def executeQuery(query):
    DB = getSqlConnection()
    cursor = DB.cursor()
    sql = query
    cursor.execute(sql)
    # return list of dic
    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    cursor.close()
    # return list of dic
    return json_data

def doInserteQuery(query):
    DB = getSqlConnection()
    cursor = DB.cursor()
    sql = query
    cursor.execute(sql)
    DB.commit()
    cursor.close()
    return 