import json
from book import Book

def saveBooks(books):
    json_books = []
    for book in books:
        json_books.append(book.to_dict())
    with open('books.dat', 'w') as file:
        file.write(json.dumps(json_books,indent=4))

def loadBooks():
    try:
        file=open("books.dat","r")
        loaded_books = json.loads(file.read())
        books = []
        for book in loaded_books:
            books.append( Book(book['id'], book['name'], book['description'], book['isbn'], book['page_count'], book['issued'], book['author'], book['year']) )
        file.close()
        return books
    except:
        return []

def addBook(book):
    books = loadBooks()
    newBook = Book(book['id'], book['name'], book['description'], book['isbn'], book['pageCount'], book['issued'], book['author'], book['year'])
    saveBooks([*books, assignValidId(books,newBook)])

def assignValidId(books, newBook):
    booksIds = []
    for book in books:
        booksIds.append(int(book.id))
    if list(filter(lambda id: int(id == newBook.id), booksIds))!=[]:
        newBook.id=int(max(booksIds)+1)
    return newBook

def find_books(id):
    books = loadBooks()
    for book in books:
        if book.id == id:
            return book
    print("Not found")
    return None
