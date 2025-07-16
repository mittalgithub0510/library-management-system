import tkinter as tk
from tkinter import messagebox
from models.library import Library
from models.book import Book
from models.user import User

library = Library()

def add_book_ui():
    def submit():
        title = title_entry.get()
        author = author_entry.get()
        isbn = isbn_entry.get()
        if library.add_book(Book(title, author, isbn)):
            messagebox.showinfo("Success", "Book added.")
            win.destroy()
        else:
            messagebox.showerror("Error", "Book already exists.")

    win = tk.Toplevel(root)
    win.title("Add Book")
    tk.Label(win, text="Title").pack()
    title_entry = tk.Entry(win)
    title_entry.pack()
    tk.Label(win, text="Author").pack()
    author_entry = tk.Entry(win)
    author_entry.pack()
    tk.Label(win, text="ISBN").pack()
    isbn_entry = tk.Entry(win)
    isbn_entry.pack()
    tk.Button(win, text="Add", command=submit).pack()

def register_user_ui():
    def submit():
        name = name_entry.get()
        uid = id_entry.get()
        if library.register_user(User(name, uid)):
            messagebox.showinfo("Success", "User registered.")
            win.destroy()
        else:
            messagebox.showerror("Error", "User already exists.")

    win = tk.Toplevel(root)
    win.title("Register User")
    tk.Label(win, text="Name").pack()
    name_entry = tk.Entry(win)
    name_entry.pack()
    tk.Label(win, text="User ID").pack()
    id_entry = tk.Entry(win)
    id_entry.pack()
    tk.Button(win, text="Register", command=submit).pack()

def borrow_book_ui():
    def submit():
        isbn = isbn_entry.get()
        uid = uid_entry.get()
        if library.borrow_book(isbn, uid):
            messagebox.showinfo("Success", "Book borrowed.")
            win.destroy()
        else:
            messagebox.showerror("Error", "Borrow failed. Book may be unavailable or user invalid.")

    win = tk.Toplevel(root)
    win.title("Borrow Book")
    tk.Label(win, text="ISBN").pack()
    isbn_entry = tk.Entry(win)
    isbn_entry.pack()
    tk.Label(win, text="User ID").pack()
    uid_entry = tk.Entry(win)
    uid_entry.pack()
    tk.Button(win, text="Borrow", command=submit).pack()

def return_book_ui():
    def submit():
        isbn = isbn_entry.get()
        uid = uid_entry.get()
        if library.return_book(isbn, uid):
            messagebox.showinfo("Success", "Book returned.")
            win.destroy()
        else:
            messagebox.showerror("Error", "Return failed. Book or user invalid.")

    win = tk.Toplevel(root)
    win.title("Return Book")
    tk.Label(win, text="ISBN").pack()
    isbn_entry = tk.Entry(win)
    isbn_entry.pack()
    tk.Label(win, text="User ID").pack()
    uid_entry = tk.Entry(win)
    uid_entry.pack()
    tk.Button(win, text="Return", command=submit).pack()

def search_book_ui():
    def submit():
        query = query_entry.get()
        results = library.search_book(query)
        result_text = "\n".join(str(book) for book in results) or "No books found."
        messagebox.showinfo("Search Results", result_text)
        win.destroy()

    win = tk.Toplevel(root)
    win.title("Search Book")
    tk.Label(win, text="Search Query").pack()
    query_entry = tk.Entry(win)
    query_entry.pack()
    tk.Button(win, text="Search", command=submit).pack()

def display_all_books_ui():
    books = [str(book) for book in library._books.values()]
    text = "\n".join(books) or "No books available."
    messagebox.showinfo("All Books", text)

def display_all_users_ui():
    users = [str(user) for user in library._users.values()]
    text = "\n".join(users) or "No users found."
    messagebox.showinfo("All Users", text)

# Root UI
root = tk.Tk()
root.title("Library Management System")

tk.Button(root, text="Add Book", command=add_book_ui, width=30).pack(pady=5)
tk.Button(root, text="Register User", command=register_user_ui, width=30).pack(pady=5)
tk.Button(root, text="Borrow Book", command=borrow_book_ui, width=30).pack(pady=5)
tk.Button(root, text="Return Book", command=return_book_ui, width=30).pack(pady=5)
tk.Button(root, text="Search Book", command=search_book_ui, width=30).pack(pady=5)
tk.Button(root, text="Display All Books", command=display_all_books_ui, width=30).pack(pady=5)
tk.Button(root, text="Display All Users", command=display_all_users_ui, width=30).pack(pady=5)

root.mainloop()
