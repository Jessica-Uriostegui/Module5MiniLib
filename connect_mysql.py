
import mysql.connector
from mysql.connector import Error 

def connect_db():
    # db connection variables
    db_name = "library_db"
    user = "root"
    password = "Dolphin25!" 
    host = "localhost"
    
    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )

        # check if the connection is successful
        if conn.is_connected():
            print("Connected to MySQL Database successfully")
            return conn
    except Error as e:
        print(f"Error: {e}")

   
connect_db()