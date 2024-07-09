# from connect_mysql import connect_db
# from mysql.connector import Error


import book
import user
import author
import genre
# create main method (driver file)
def main(): 
    while True:
        # greeting with menu with options
        print("""
            Welcome! What would you like to do: 
        1. Add Author with Biography
        2. Add Genre    
        3. Add Book
        4. Checkout A Book
        5. Search A Book
        6. Display All Books
        7. View Author Details
        8. Display All Authors
        9. Add User
        10. View User Details
        11. Display All Users
        12. Return A Book
        13. Exit
        """)
        print("******************************************** \n")
        
        choice = input("Enter your choice: \n")
        
        try:
            if choice == "1":
                author.add_author()
            elif choice == "2":
                genre.add_genre()
            elif choice == "3":
                book.add_book()
            elif choice == "4":
                book.check_out()
            elif choice == "5":
                book.search_book()
            elif choice == "6":
                book.display_books()
            elif choice == "7":
                author.view_author_details()
            elif choice == "8":
                author.display_authors()
            elif choice == "9":
                user.add_user()
            elif choice == "10":
                user.view_user_details()
            elif choice == "11":
                user.display_users()
            elif choice == "12":
                book.return_book()
            elif choice == "13":
                print("Thank you have a great day. Good bye.")
                break
            else:
                print("Invalid choice")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
