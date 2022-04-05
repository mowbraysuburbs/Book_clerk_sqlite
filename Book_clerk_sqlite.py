
""" 
Capstone 1 (Level 2 Task 6) SUMMARY:

This program is used a bookstore cledrk

The program can do the following functions:

1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit

"""

import sqlite3


#Connect to book database
db = sqlite3.connect('books_db')
c = db.cursor()  # Get a cursor object'

"""
The code below shows the format of the table.
Made a doc string as the table has already been created.

# c.execute('''
# CREATE TABLE books(
# id INTEGER PRIMARY KEY,   
# Title TEXT,
# Author TEXT,
# Qty INTEGER)
# ''')

# db.commit()
# db.close()

"""

# The current books in the table
book_data = [
(3001, "A Tale of Two Cities", "Charles Dickens", 30),
(3002, "Harry Potter and the Philospher's Stone", "J.K. Rowling", 40),
(3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 37),
(3004, "Lord of the Rings", "J.R.R Tolkien", 37),
(3005, "Alice in Wonderland", "Lewis Carroll", 12)
]


def book_enter(id, title, author, qty):
    '''
    Function used for entering new book
    All the information is required here i.e. 
    ID, title, author and qty,
    PRIMARY KEYS (i.e. ID) cannot be duplicated 
    thus we use the try function to check
    '''

    c.execute('''SELECT id FROM books
    WHERE id = ? 
    ''', (id,))

    #find_id is the fetched ID
    find_id = c.fetchone()

    """
    If find_id = None it means id is unique
    #if statement checks for uniqueness
    """

    if find_id == None: 
        print("\nID is valid!\n")
    else: 
        #Turns find_id into string
        #This only happens when the id exists in db
        for word in find_id: find_id = word
    
    #while loop checks for unique ID
    while find_id == id:
        
        id = int(input("ID already in database - choose new ID: "))

        c.execute('''SELECT id FROM books
        WHERE id = ? 
        ''', (id,))

        try:

            find_id = c.fetchone()
            for word in find_id: find_id = word
        
        #TypeError as None is not iterable
        except TypeError:
            print("ID is valid")

    #adds new book info
    c.execute('''
    INSERT into books
    VALUES (?, ?, ?, ?)
    ''', (id, title, author, qty))

    db.commit()

    #Prints out whole database
    c.execute("SELECT * FROM books")
    data = c.fetchall()
    for item in data: print(item) 


def book_update(id):      
    '''
    Updating the book could be the information or 
    the amount of books that are in stock. 

    I assumed that all the information will have to changed regardless
    whether it is the same or not. 

    It is assumed that the bookclerk knows the ID as it is on the phy. book 
    or they will have to search the book's id using the search method
    '''

    book = c.execute('''SELECT * FROM books WHERE id = ?''', (id,))

    #Displays current info of chosen book that req. updating
    book = c.fetchone()
    print(book)

    #New parameters
    id_new = int(input("What is the new ID of new book? "))
    title_new = str(input("What is the new title? "))
    author_new = str(input("What is the new author? "))
    qty_new = int(input("What is the new qty? "))

    c.execute('''UPDATE books
    SET id = ?,
        title = ?,
        author = ?,
        qty = ?
    WHERE id = ?
    ''',(id_new, title_new, author_new, qty_new,id))

    db.commit()

    #Prints new book information
    book = c.execute('''SELECT * FROM books WHERE id = ?''', (id_new,))
    book = c.fetchone()
    print("\nbook has been updated")
    print(book)


def book_del(id):       
    '''
    Deletes book based on its resp. ID
    It is assumed that the bookclerk knows the ID as it is on the phy. book 
    or they will have to search the book's id using the search method
    '''

    c.execute('''DELETE FROM books
    WHERE id = ? 
    ''',(id,))

    db.commit()    

    #Prints out the whole table to check if book is deleted
    c.execute("SELECT * FROM books")
    data = c.fetchall()
    for item in data: print(item) 
    c.close 

def book_search(id, title, author):

    '''
    Deletes book from database
    It is assumed that the bookclerk knows the ID as it is on the phy. book 
    or they will have to search the book's id using the search method
    '''

    #% looks for variations on boths sides of the word/number
    id = "%"+id+"%"
    title = "%"+title+"%"
    author = "%"+author+"%"

    meta = ["ID", "Title", "Author", "Qty"]

    #LIKE function search for similar variables
    c.execute('''SELECT * FROM books
    WHERE id LIKE ? 
    AND Author LIKE ?

    ''', (id, author,))

    books = c.fetchall()

    for book in books:
    
        for i in range(len(book)):
            print(f"{meta[i]}: {book[i]}")
            # print("\n") 


'''
The question variable along with the while loop introduces the user
to the program.

question input triggers the respective functions
'''

question = str(input(

"""
Welcome to bookstore software!

What would you like to do 
(enter/update/delete/search/exit): """)
)

while question != "exit":

    if question == "enter":

        id = int(input("What is the ID of new book? "))
        title = str(input("What is book name? "))
        author = str(input("What is Author name? "))
        qty = int(input("What is the quantity? "))

        book_enter(id, title, author, qty)

        break

    elif question == "update":

        id = int(input("What is the ID of book? "))

        book_update(id)
  
        break

    elif question == "delete":

        id = int(input("What is the ID? "))

        book_del(id)

        break

    elif question == "search":
        
        print(
"""
If you do not know the info, you may leave it blank
Please enter the keywords when prompt. """)

        id = str(input("What is the id: "))
        title = str(input("What is the title of the book: "))       
        author = str(input("What is the author: "))        
            
        book_search(id, title, author)

        break

    elif question == "exit":
        print("Goodbye")
        break

    else:

        print("\nOops - incorrect input")
        
        question = str(input(
"""
What would you like to do 
(enter/update/delete/search/exit): """))


# REFERENCES

# https://stackoverflow.com/questions/4409539/pythonsqlite-the-like-query-with-wildcards
# https://www.tutorialspoint.com/sqlite/sqlite_where_clause.htm
# https://stackoverflow.com/questions/39372932/python-sqlite3-update-set-from-variables