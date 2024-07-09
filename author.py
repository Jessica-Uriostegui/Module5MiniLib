from connect_mysql import connect_db
from mysql.connector import Error, IntegrityError
       
# funtion for adding author
def add_author():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        name = input("Enter the author's name: \n").capitalize()
        biography = input("Enter the author's biography: \n").capitalize()
        
        query_check = "SELECT author_id FROM authors WHERE name =  %s"
        cursor.execute(query_check, (name,))
        result = cursor.fetchone()
        # used to avoid adding same author
        if result:
            print(f"Author '{name}' already exists with ID: {result[0]}")
        else:
            query_insert = "INSERT INTO authors (name,biography) Values (%s, %s)"
            cursor.execute(query_insert, (name, biography))
            conn.commit()
            print(f"Author '{name}' added to the library.")
            display_authors()
    except IntegrityError:
        print(f"Author '{name}' already exists.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def display_authors():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        query = "SELECT author_id, name FROM authors"
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            print("Available Authors:")
            for author_id, name in results:
                print(f"ID: {author_id}, Name: {name}")
        else:
            print(f"No authors available at this moment.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def view_author_details():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        name = input("Enter the author's name: \n").capitalize()

        query = "SELECT * FROM authors WHERE name = %s"
        cursor.execute(query, (name,))
        results = cursor.fetchall()
        if results:
            for result in results:
                author_id, name, biography = result
                print(f"ID: {author_id}, Name: {name}, Biography: {biography}")
        else:
            print(f"No authors available at this moment.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()