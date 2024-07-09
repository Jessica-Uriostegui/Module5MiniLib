from connect_mysql import connect_db
from mysql.connector import Error
# imports nedded
import author
import genre
from datetime import date
# function for adding book
def add_book():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        # used to make sure author was added first
        cursor.execute("SELECT COUNT(*) FROM authors")
        author_count = cursor.fetchone()[0]
        if author_count == 0:
            print("No authors found. Please add authors first.")
            return
        # used to make sure a genre was added first
        cursor.execute("SELECT COUNT(*) FROM genres")
        genre_count = cursor.fetchone()[0]
        if genre_count == 0:
            print("No genres found. Please add genres first.")
            return
        
        title = input("Enter the book's title: \n").capitalize()
        
        while True:
            # Display available authors
            cursor.execute("SELECT author_id, name From authors")
            authors = cursor.fetchall()
            print("Available Authors:")
            for author_id, name in authors:
                print(f"ID:{author_id}, Name: {name}")
            
            author_id_input = input("Enter the author's ID (or 'add' to add new author): \n")
            if author_id_input.lower() == 'add':
                author.add_author()
                continue
            
            cursor.execute("SELECT * FROM authors WHERE author_id = %s", (author_id_input,))
            if cursor.fetchone():
                author_id = int(author_id_input)
                break
            else:
                print("Invalid author ID. PLease enter a valid ID or add new author")

        while True:
            cursor.execute("SELECT genre_id, genre_name FROM genres")
            genres = cursor.fetchall()
            print("Available Genres:")
            for genre_id, genre_name in genres:
                print(f"ID: {genre_id}, Name: {genre_name}")

            genre_id_input = input("Enter the genre's ID (or 'add' to add new genre): \n")
            if genre_id_input.lower() == 'add':
                genre.add_genre()
                continue

            cursor.execute("SELECT * FROM genres WHERE genre_id = %s", (genre_id_input,))
            if cursor.fetchone():
                genre_id = int(genre_id_input)
                break
            else:
                print("Invalid genre ID. Please enter a valid ID or add a new genre.")

        publication_date = input("Enter the book's publication_date (YYYY-MM-DD): \n")
        
        query = """
        INSERT INTO books (title, author_id, genre_id, publication_date) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (title, author_id, genre_id, publication_date)) #prepares query with arguments
        conn.commit() #commits and sends changes to our database
        print(f"Book '{title}' added to the library.")
   
    except Error as e:
        print(f"Error: {e}")

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# check out fuuntion
def check_out():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        title = input("Please enter the book you would like to check out: \n").capitalize()
        library_id = input("Please enter library id (e.g., 12-123-12 ): \n").replace('-', '') 
        
        
        user_query = "SELECT user_id FROM users WHERE library_id = %s"
        cursor.execute(user_query, (library_id,))
        user_result = cursor.fetchone()
        
        if not user_result:
            print("User not found")
            return
        
        user_id = user_result[0]
        loan_date = date.today()

        book_query = "SELECT book_id, is_available FROM books WHERE title = %s"
        cursor.execute(book_query, (title,))
        book_result = cursor.fetchone()

        if book_result and book_result[1]:
            book_id = book_result[0]
            update_query = "UPDATE books SET is_available = FALSE WHERE book_id = %s"
            cursor.execute(update_query, (book_id,))
            loan_query = "INSERT INTO loans (book_id, user_id, loan_date) VALUES (%s, %s, %s)"
            cursor.execute(loan_query, (book_id, user_id, loan_date))
            conn.commit()
            print(f"Book '{title}' has been checked out to {library_id}.")
        else:
            print("Book is not available or not found. ")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
        
# function for returning books
def return_book():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        title = input("Enter the title of the book you would like to return: \n").capitalize()
        library_id = input("Please enter library id (e.g., 12-123-12 ): \n").replace('-', '')
        
        query = """
        SELECT loans.loan_id, books.book_id 
        FROM loans
        JOIN books ON loans.book_id = books.book_id
        JOIN users ON loans.user_id = users.user_id
        WHERE books.title = %s AND users.library_id = %s
    """
        cursor.execute(query, (title, library_id,))
        result = cursor.fetchone()

        if result:
            loan_id, book_id = result
            delete_query = "DELETE FROM loans WHERE loan_id = %s"
            cursor.execute(delete_query, (loan_id,))
            update_query = "UPDATE books SET is_available = TRUE WHERE book_id = %s"
            cursor.execute(update_query, (book_id,))
            conn.commit()
            print(f"Book '{title}' has been successfully returned")
        else:
            print("Invalid return. The book title is incorrect or user Id does not match")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
        
def search_book():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        title = input("What is the title you're looking for? \n").capitalize()
        
        query = "SELECT * FROM books WHERE title LIKE %s"
        cursor.execute(query, ('%' + title + '%',))
        results = cursor.fetchall()

        if results:
            for (book_id, title, author, genre, publication_date, is_available) in results:
                status = "Available" if is_available else "Borrowed"
                print(f"ID: {book_id}, Title: {title}, Author: {author}, Genre: {genre}, Published: {publication_date}, Status: {status}")
        else:
            print("Sorry! That book is not in our library.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def display_books():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT * FROM books"
        cursor.execute(query)
        results = cursor.fetchall()

        for (book_id, title, author, genre, publication_date, is_available) in results:
                status = "Available" if is_available else "Borrowed"
                print(f"ID: {book_id}, Title: {title}, Author: {author}, Genre: {genre}, Published: {publication_date}, Status: {status}")
                return
        else: 
            print(f"No books available at this time.")
       
    
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()



   



        
