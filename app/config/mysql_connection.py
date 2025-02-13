import mysql.connector
from mysql.connector import Error

def create_connection():
    """Membuat koneksi ke database MySQL."""
    try:
        connection = mysql.connector.connect(
            host="localhost",         
            user="your_username", 
            password="your_password",
            database="your_database" 
        )
        
        if connection.is_connected():
            print("Koneksi berhasil!")
        return connection

    except Error as err:
        print(f"Terjadi error: {err}")
        return None

def close_connection(connection):
    """Menutup koneksi MySQL."""
    if connection.is_connected():
        connection.close()
        print("Koneksi ditutup.")
