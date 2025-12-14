import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR PASSWORD",
        database="bank_management"
    )
    return connection

