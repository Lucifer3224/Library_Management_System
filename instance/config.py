# db_connection.py

import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="username",
            password="password",
            database="database name",
            auth_plugin='mysql_native_password'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {str(e)}")
        return None

