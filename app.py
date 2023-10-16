import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, strOfAuthors

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///lionbooks.db")

# # Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show all of user's books"""
    # If request via GET, display user's books
    if request.method == "GET":
        # Obtain information of each book user owns to display
        myBooks = db.execute("SELECT isbn, title, authors, cover FROM library WHERE user_id = ?", session["user_id"])

        # Obtain user's name to say hello
        name = db.execute("SELECT name FROM users WHERE id = ?", session["user_id"])[0]['name']

        return render_template("index.html", books=myBooks, name=name)

    else:
        # If request via POST (user clicked on "details" button in each row)
        if request.form.get("details"):

            # Lookup book info
            isbn = request.form.get("details")
            volumes = lookup(isbn)

            # If successful, display book info
            return render_template("info.html", title=volumes["title"], authors=volumes["authors"], cover=volumes["cover"], description=volumes["description"], isbn=isbn)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # If user uses GET request method, go to form to register
    if request.method == "GET":
        return render_template("register.html")

    # If user submits form and access via POST
    else:
        # Check submissions are not blank
        if not request.form.get("username"):
            return apology("must provide username", 400)

        if not request.form.get("email"):
            return apology("must provide email", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Check password verification
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # Query for username
        found = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Check if username is already taken
        if len(found) != 0:
            return apology("username is not available", 400)

        # Hash password to store
        hash = generate_password_hash(request.form.get("password"))

        # INSERT new user row to table
        rows = db.execute('INSERT INTO users (username, hash, email, name) VALUES (?, ?, ?, ?)',
                          request.form.get("username"), hash, request.form.get("email"), request.form.get("name"))

        # Save user ID to remember which user has logged in
        session["user_id"] = rows

        # Redirect to home page
        return redirect("/")


@app.route("/search")
@login_required
def search():
    """Search for books through isbn"""

    # Obtain isbn from form
    isbn = request.args.get("isbn")

    # Lookup isbn for book information
    volumes = lookup(isbn)

    # Check if lookup was successful/isbn exists
    if volumes is not None:
        # title, authors, cover, description = volumes  # Unpack the tuple
        return render_template("info.html", title=volumes["title"], authors=volumes["authors"], cover=volumes["cover"], description=volumes["description"],
                               isbn=isbn)
    else:
        return apology("isbn does not exist", 400)
    # if volumes == None:
    #     return apology("isbn does not exist", 400)
    #
    # # If successful, display book info
    # return render_template("info.html", title=volumes["title"], authors=volumes["authors"], cover=volumes["cover"], description=volumes["description"], isbn=isbn)


@app.route("/info")
@login_required
def info():
    """Handle a book from its info page"""

    # Obtain user email to later store in library
    email = db.execute("SELECT email FROM users WHERE id = ?", session["user_id"])[0]['email']

    # For each button available, initalize isbn and shelf
    if request.args.get("add"):
        isbn = request.args.get("add")
        shelf = None

    elif request.args.get("currRead"):
        isbn = request.args.get("currRead")
        shelf = "currentlyReading"

    elif request.args.get("wantToRead"):
        isbn = request.args.get("wantToRead")
        shelf = "wantToRead"

    elif request.args.get("alrRead"):
        isbn = request.args.get("alrRead")
        shelf = "read"

    # If the button clicked was not "remove", then proceed with adding the book into tables
    if not request.args.get("remove"):
        # Lookup book info
        volumes = lookup(isbn)

        # Obtain string version of author(s) to store in database as TEXT
        authorsStr = strOfAuthors(volumes["authors"])

        # Add book to database
        db.execute("INSERT INTO myBooks (user_id, isbn, shelf) VALUES (?, ?, ?)", session["user_id"], isbn, shelf)
        db.execute("INSERT INTO library (user_id, isbn, user_email, title, authors, cover) VALUES (?, ?, ?, ?, ?, ?)",
                   session["user_id"], isbn, email, volumes["title"], authorsStr, volumes["cover"])

    # User chose to remove that book from her books
    else:
        # Obtain isbn
        isbn = request.args.get("remove")

        # Lookup book info
        volumes = lookup(isbn)

        # Obtain string version of author(s) to store in database as TEXT
        authorsStr = strOfAuthors(volumes["authors"])

        # Check if book user wants to remove is actually owned
        bookExists = db.execute("SELECT COUNT(isbn) FROM library WHERE user_id = ? AND isbn = ?", session["user_id"], isbn)

        if int(bookExists[0]['COUNT(isbn)']) > 0:
            # Make sure only one book is deleted at a time
            db.execute("DELETE FROM myBooks WHERE user_id = ? AND isbn = ?", session["user_id"], isbn)
            db.execute("DELETE FROM library WHERE user_id = ? AND isbn = ? AND user_email = ? AND title = ? AND authors = ? AND cover = ?",
                       session["user_id"], isbn, email, volumes["title"], authorsStr, volumes["cover"])
        else:
            return apology("user does not own book", 400)

    return redirect("/")


# Routes for all the shelves:
@app.route("/currentlyreading")
@login_required
def currentlyreading():
    """Display Currently Reading books"""

    # If request via GET, display user's books
    if request.method == "GET":
        # Obtain book info
        myBooks = db.execute("SELECT library.isbn, title, authors, cover FROM library WHERE user_id = ? AND isbn IN (SELECT myBooks.isbn FROM myBooks WHERE shelf = ?)",
                             session["user_id"], "currentlyReading")

        return render_template("currentlyreading.html", books=myBooks)

    else:
        # If request via POST (user clicked on details button for a specific book)
        if request.form.get("details"):

            # Lookup book info
            isbn = request.form.get("details")
            volumes = lookup(isbn)

            # Display book info
            return render_template("info.html", title=volumes["title"], authors=volumes["authors"], cover=volumes["cover"], description=volumes["description"], isbn=isbn)


@app.route("/wanttoread")
@login_required
def wanttoread():
    """Display Want To Read books"""

    # If request via GET, display user's books
    if request.method == "GET":
        # Obtain book info
        myBooks = db.execute(
            "SELECT library.isbn, title, authors, cover FROM library WHERE user_id = ? AND isbn IN (SELECT myBooks.isbn FROM myBooks WHERE shelf = ?)", session["user_id"], "wantToRead")

        return render_template("wanttoread.html", books=myBooks)

    else:
        # If request via POST (user clicked on details button for a specific book)
        if request.form.get("details"):

            # Lookup book info
            isbn = request.form.get("details")
            volumes = lookup(isbn)

            # Display book info
            return render_template("info.html", title=volumes["title"], authors=volumes["authors"], cover=volumes["cover"], description=volumes["description"], isbn=isbn)


@app.route("/read")
@login_required
def read():
    """Display Read books"""

    # If request via GET, display user's books
    if request.method == "GET":
        # Obtain book info
        myBooks = db.execute(
            "SELECT library.isbn, title, authors, cover FROM library WHERE user_id = ? AND isbn IN (SELECT myBooks.isbn FROM myBooks WHERE shelf = ?)", session["user_id"], "read")

        return render_template("read.html", books=myBooks)

    else:
        # If request via POST (user clicked on details button for a specific book)
        if request.form.get("details"):

            # Lookup book info
            isbn = request.form.get("details")
            volumes = lookup(isbn)

            # Display book info
            return render_template("info.html", title=volumes["title"], authors=volumes["authors"], cover=volumes["cover"], description=volumes["description"], isbn=isbn)


@app.route("/library")
def library():
    """Display library page"""
    # Log-in not required for those only interested in borrowing books

    # If request via GET, display library
    if request.method == "GET":
        # Obtain book info
        myBooks = db.execute("SELECT isbn, title, authors, cover FROM library")

        # Obtain emails to allow users to contact the book owners
        emails = db.execute("SELECT user_email FROM library")

        return render_template("library.html", books=myBooks, emails=emails)

    else:
        # If request via POST (user clicked on details button for a specific book)
        if request.form.get("details"):

            # Lookup book info
            isbn = request.form.get("details")
            volumes = lookup(isbn)

            # If successful, display book info
            return render_template("info.html", title=volumes["title"], authors=volumes["authors"], cover=volumes["cover"], description=volumes["description"], isbn=isbn)

if __name__ == '__main__':
    app.run(debug=True)

""" Added tables in SQL:

CREATE TABLE users (
    id  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    name TEXT,
    email TEXT,
    hash TEXT NOT NULL
);

CREATE UNIQUE INDEX username ON users (username);

CREATE TABLE library (
    isbn TEXT NOT NULL,
    user_id INTEGER,
    user_email TEXT,
    title TEXT NOT NULL,
    authors TEXT NOT NULL,
    cover VARCHAR NOT NULL
);

CREATE TABLE myBooks (
    user_id INTEGER,
    isbn TEXT,
    shelf TEXT
);

"""
