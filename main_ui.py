from PyQt5.QtCore import *
from PyQt5.uic import *
from PyQt5.QtWidgets import *
from book import Book
from createDialog import Ui_createDialog
from editDialog import Ui_editDialog
from deleteDialog import Ui_deleteDialog
from mainWindow import Ui_main
import logic
from stylesheets import main_style_sheet

class mainWindow (QMainWindow, Ui_main):
    
    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setupUi(self)
        self.loadIssuedBooks()
        self.loadUnissuedBooks()
        self.loadAllBooks()
        self.newBookButton.pressed.connect(self.showAddDialog)
        self.refreshIssuedButton.pressed.connect(self.loadIssuedBooks)
        self.editIssuedButton.pressed.connect(lambda:self.editBook(self.issuedTable))
        self.editUnissuedButton.pressed.connect(lambda:self.editBook(self.unissuedTable))
        self.refreshUnissuedButton.pressed.connect(self.loadUnissuedBooks)
        self.refreshButton.pressed.connect(self.loadAllBooks)
        self.deleteIssuedButton.pressed.connect(lambda:self.showDelete(self.issuedTable))
        self.deleteUnissuedButton.pressed.connect(lambda:self.showDelete(self.unissuedTable))
        self.searchButton.pressed.connect(self.searchBook)
        self.setStyleSheet(main_style_sheet)


    def showAddDialog(self):
        createDialog = addDialog()
        createDialog.ui.buttonBox.accepted.connect(
            lambda: self.createBook(createDialog.ui)
        )
        createDialog.exec()

    def createBook(self, ui):
        book ={
            'id' : int(ui.idInput.text()),
            'name' : ui.nameInput.text(),
            'description' : ui.descriptionInput.text(),
            'isbn' : ui.isbnInput.text(),
            'pageCount' : int(ui.pageCountInput.text()),
            'issued' : ui.yesButton.isChecked(),
            'author' : ui.authorInput.text(),
            'year' : int(ui.yearInput.text())
        }
        for attribute in book:
            if book[attribute]==None or str(book[attribute])=="":
                return None
        logic.addBook(book)

    def loadIssuedBooks(self):
        books = logic.loadBooks()
        issuedBooks = list(filter(lambda book : book.issued==True, books))
        self.issuedTable.setRowCount(len(issuedBooks))
        for index, book in enumerate(issuedBooks):
            book = book.to_dict()
            for book_index, attribute in enumerate(book):
                self.issuedTable.setItem(index, book_index, QTableWidgetItem(str(book[str(attribute)])))
                self.issuedTable.item(index,book_index).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                
    def loadUnissuedBooks(self):
        books = logic.loadBooks()
        unissuedBooks = list(filter(lambda book : book.issued==False, books))
        self.unissuedTable.setRowCount(len(unissuedBooks))
        for index, book in enumerate(unissuedBooks):
            book = book.to_dict()
            for book_index, attribute in enumerate(book):
                self.unissuedTable.setItem(index, book_index, QTableWidgetItem(str(book[str(attribute)])))
                self.unissuedTable.item(index,book_index).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def loadAllBooks(self):
        books = logic.loadBooks()
        self.allBooksTable.setRowCount(len(books))
        for index, book in enumerate(books):
            book = book.to_dict()
            for book_index, attribute in enumerate(book):
                self.allBooksTable.setItem(index, book_index, QTableWidgetItem(str(book[str(attribute)])))
                self.allBooksTable.item(index,book_index).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def editBook(self, table):
        selectedRow = table.currentRow()
        if int(selectedRow) != -1:
            id = int(table.item(selectedRow,0).text())
            book = logic.find_books(id)
            editdialog = editDialog()
            editdialog.ui.idInput.setValue(book.id)
            editdialog.ui.nameInput.setText(book.name)
            editdialog.ui.descriptionInput.setText(book.description)
            editdialog.ui.isbnInput.setText(book.isbn)
            editdialog.ui.pageCountInput.setValue(book.page_count)
            if book.issued:
                editdialog.ui.yesButton.setChecked(True)
            else:
                editdialog.ui.noButton.setChecked(True)
            editdialog.ui.authorInput.setText(book.author)
            editdialog.ui.yearInput.setValue(book.year)
            editdialog.ui.buttonBox.accepted.connect(
                lambda: self.overwriteBook(editdialog.ui)
            )
            editdialog.exec()

    def overwriteBook(self, ui):
        newBook = Book(
            int(ui.idInput.text()),
            ui.nameInput.text(),
            ui.descriptionInput.text(),
            ui.isbnInput.text(),
            int(ui.pageCountInput.text()),
            ui.yesButton.isChecked(),
            ui.authorInput.text(),
            int(ui.yearInput.text())
        )
        books = logic.loadBooks()
        books = list(filter(lambda book: int(book.id) != int(newBook.id),books))
        books.append(newBook)
        logic.saveBooks(books)

    def showDelete(self, table):
        selectedRow = table.currentRow()
        if int(selectedRow) != -1:
            delDialog = deleteDialog()
            delDialog.ui.buttonBox.accepted.connect(lambda: self.deleteBook(table))
            delDialog.exec()            

    def deleteBook(self, table):
        selectedRow = table.currentRow()
        if int(selectedRow) != -1:
            books = logic.loadBooks()
            id = int(table.item(selectedRow,0).text())
            books = list(filter(lambda book: book.id != id, books))
            logic.saveBooks(books)

    def searchBook(self):
        if self.searchInput.text()!="":
            id=int(self.searchInput.text())
            books = logic.loadBooks()
            books = list(filter(lambda book : book.id == id, books))
            self.findBooksTable.setRowCount(1)
            book=books[0].to_dict()
            for book_index, attribute in enumerate(book):
                self.findBooksTable.setItem(0, book_index, QTableWidgetItem(str(book[str(attribute)])))
                self.findBooksTable.item(0,book_index).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

class addDialog (QDialog):

    def __init__(self, parent=None):
        super(addDialog,self).__init__(parent)
        self.ui = Ui_createDialog()
        self.setStyleSheet(main_style_sheet)
        self.ui.setupUi(self)


class editDialog (QDialog):

    def __init__(self, parent=None):
        super(editDialog,self).__init__(parent)
        self.ui = Ui_editDialog()
        self.setStyleSheet(main_style_sheet)
        self.ui.setupUi(self)

class deleteDialog (QDialog):

    def __init__(self, parent=None):
        super(deleteDialog,self).__init__(parent)
        self.ui = Ui_deleteDialog()
        self.setStyleSheet(main_style_sheet)
        self.ui.setupUi(self)

app = QApplication([])
window = mainWindow()
window.show()
app.exec()