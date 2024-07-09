from connect_mysql import connect_db
from mysql.connector import Error, IntegrityError
# menu for choosing a genre
def add_genre():
    genre_options = {
            "1": "Biography",
            "2": "Comic/Manga",
            "3": "Fantasy",
            "4": "Fiction",
            "5": "Humor",
            "6": "Childern's",
            "7": "Romance",
            "8": "Science Fiction",
            "9": "Short Story",
            "10": "Non Fiction"
        }
        
    try:    
        genre_number = input(
            "Enter the genre:\n1. Biography \n2. Comic/Manga \n3. Fantasy \n4.Fiction \n5.Humor \n6. Childrens \n7. Romance \n8. Science Fiction \n9.Short Story \n10. Non Fiction \n"
            )
        
        genre_name = genre_options.get(genre_number)

        if not genre_name:
            print("Invalid genre number. Please try again.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        
        query = "INSERT INTO genres (genre_name) VALUES (%s)"
        cursor.execute(query, (genre_name,))
        conn.commit()
        print(f"Genre '{genre_name}' added to the library.")
        # to make sure same genre is not added again
        display_genres()
    except IntegrityError:
        print(f"Genre '{genre_name}' already exists.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def display_genres():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        query = "SELECT genre_id, genre_name FROM genres"
        cursor.execute(query)
        results = cursor.fetchall()
        
        print("Available Genres:")
        for genre_id, genre_name in results:
            print(f"ID {genre_id}, Name: {genre_name}")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
