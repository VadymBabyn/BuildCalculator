import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='building_cost_db'
    )
    return connection
