from connect_mysql import connect_db
from mysql.connector import Error
# function to add user
def add_user():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        
        name = input("Enter user's name: \n").capitalize()
        library_id = int(input("Enter the user's library ID (e.g., 12-123-12 ): \n").replace('-', ''))
        
        
        query = "INSERT INTO users (name, library_id) VALUES (%s, %s)"
        cursor.execute(query, (name, library_id))
        conn.commit()
        print(f"User '{name}' added to the library.")
    
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
def display_users():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT * FROM users"
        cursor.execute(query)
        results = cursor.fetchall()
        
        for (user_id, name, library_id) in results:
            print(f"Name: {name}, Library ID: {library_id}")
        else:
            print("No registered Users.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    

def view_user_details():
    try:
        library_id = int(input("Enter the user's library ID (e.g., 12-123-12 ): \n").replace('-', ''))
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE library_id = %s" 
        cursor.execute(query, (library_id,))
        result = cursor.fetchone()
        
        if result:
            user_id, name, library_id = result
            print(f"Name: {name}, Library ID: {library_id}")
        else:
            print("User not found.") 
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
 