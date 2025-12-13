import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="gaurav@123",
        database="bank_management"
    )
    return connection
