from book import Book
import os
import json
import logic

def print_options():
    print("What do you want to do?")
    print("1:Create a book")
    print("2:Save the books localy")
    print("3:Load books from disk")
    print("4:Issue book")
    print("5:Return book")
    print("6:Update book")
    print("7:Show all books")
    print("8:Find books by id")
    print("0:Exit")

def create_book():
    print("Please enter the atributes")
    id=input("Id:")
    name=input("Name:")
    description=input("Description:")
    isbn=input("ISBN:")
    page_count=int(input("Page count:"))
    issued=input("Issued? (y/n):")
    issued=(issued=="y" or issued=="Y")
    author=input("Author:")
    year=input("Year:")
    book= Book(id, name, description, isbn, page_count, issued, author, year)
    return book

def update_book(id):
    book=logic.find_books(id)
    if book != None:
        books[index] = create_book()
        print("Done")
    else:
        print("ID not found")


option=1
books=[]
while option!=0:
    print_options()
    option=int(input("Type your option:"))

    if option==1:
        books.append(create_book())
    
    elif option==2:
        logic.saveBooks(books)

    elif option==3:
        for book in logic.loadBooks():
            books.append(book)
            print(book.to_dict())

    elif option==4:
        id=input("Type the id: ")
        index=logic.find_books(id)
        if index!=None:
            books[index].issued=True
            print("Done")
        else:
            print("The id doesnt exist")

    elif option==5:
        id=input("Type the id: ")
        index=logic.find_books(id)
        if index!=None:
            books[index].issued=False 
            print("Done")
        else:
            print("The id doesnt exist")

    elif option==6:
        id=input("Type the id: ")
        update_book(id)
    
    elif option==7:
        for book in books:
            print(book.to_dict())    
            
    elif option ==8:
        id = input("Type the id: ")
        print(books[logic.find_books(id)].to_dict())
    
    elif option!=0:
        print("The option doesnt exist")

    input("Press enter to continue ")
    os.system("cls")
