import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify,url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, strOfAuthors
import csv
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///lionbooks.db")

# with open('mock_data.csv', 'r') as file:
#     csv_reader = csv.reader(file)
#     next(csv_reader)  # Skip header row if needed
#     for row in csv_reader:
#         db.execute('INSERT INTO rating (username, isbn, rating) VALUES (?, ?, ?)', int(row[0]), row[1], int(row[2]))

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
            comments = db.execute("SELECT user_id, comment FROM comments WHERE isbn = ?", isbn)

            # If successful, display book info
            return render_template("info.html", title=volumes["title"], authors=volumes["authors"], cover=volumes["cover"], description=volumes["description"], isbn=isbn,comments=comments)


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
def info(isbn="",shelf=None):
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
        myBooks = db.execute("SELECT DISTINCT library.isbn, title, authors, cover FROM library WHERE user_id = ? AND isbn IN (SELECT myBooks.isbn FROM myBooks WHERE shelf = ?)",
                             session["user_id"], "currentlyReading")

        return render_template("currentlyreading.html", books=myBooks)

    else:
        # If request via POST (user clicked on details button for a specific book)
        if request.form.get("details"):

            # Lookup book info
            isbn = request.form.get("details")
            volumes = lookup(isbn)
            comments = db.execute("SELECT user_id, comment FROM comments WHERE isbn = ?", isbn)

            # Display book info
            return render_template("info.html", title=volumes["title"], authors=volumes["authors"], cover=volumes["cover"], description=volumes["description"], isbn=isbn,comments=comments)


@app.route("/wanttoread")
@login_required
def wanttoread():
    """Display Want To Read books"""

    # If request via GET, display user's books
    if request.method == "GET":
        # Obtain book info
        myBooks = db.execute(
            "SELECT DISTINCT library.isbn, title, authors, cover FROM library WHERE user_id = ? AND isbn IN (SELECT myBooks.isbn FROM myBooks WHERE shelf = ?)", session["user_id"], "wantToRead")

        return render_template("wanttoread.html", books=myBooks)

    else:
        # If request via POST (user clicked on details button for a specific book)
        if request.form.get("details"):

            # Lookup book info
            isbn = request.form.get("details")
            volumes = lookup(isbn)
            comments = db.execute("SELECT user_id, comment FROM comments WHERE isbn = ?", isbn)

            # Display book info
            return render_template("info.html", title=volumes["title"], authors=volumes["authors"], cover=volumes["cover"], description=volumes["description"], isbn=isbn,comments=comments)


@app.route("/read")
@login_required
def read():
    """Display Read books"""

    # If request via GET, display user's books
    if request.method == "GET":
        # Obtain book info
        myBooks = db.execute(
            "SELECT DISTINCT library.isbn, title, authors, cover FROM library WHERE user_id = ? AND isbn IN (SELECT myBooks.isbn FROM myBooks WHERE shelf = ?)", session["user_id"], "read")

        return render_template("read.html", books=myBooks)

    else:
        # If request via POST (user clicked on details button for a specific book)
        if request.form.get("details"):

            # Lookup book info
            isbn = request.form.get("details")
            volumes = lookup(isbn)
            comments = db.execute("SELECT user_id, comment FROM comments WHERE isbn = ?", isbn)

            # Display book info
            return render_template("info.html", title=volumes["title"], authors=volumes["authors"], cover=volumes["cover"], description=volumes["description"], isbn=isbn,comment=comments)


@app.route("/library")
def library():
    get_recommendations()
    """Display library page"""
    # Log-in not required for those only interested in borrowing books

    # If request via GET, display library
    if request.method == "GET":
        # Obtain book info
        myBooks = db.execute("SELECT DISTINCT isbn, title, authors, cover FROM library")
        # Create a dictionary to store book ratings by ISBN
        book_ratings = {}

        # Fetch and store the rating for each book
        for book in myBooks:
            isbn = book['isbn']
            # Fetch the rating for the book
            rating = db.execute("SELECT rating FROM rating WHERE isbn = ? AND username = ?", isbn,session["user_id"])
            # If a rating exists, store it in the dictionary
            if rating:
                book_ratings[isbn] = int(rating[0]["rating"])
            else:
                # If no rating exists, set it to 0
                book_ratings[isbn] = 0
        # Obtain emails to allow users to contact the book owners
        emails = db.execute("SELECT user_email FROM library")

        return render_template("library.html", books=myBooks, emails=emails,book_ratings = book_ratings)

    else:
        # If request via POST (user clicked on details button for a specific book)
        if request.form.get("details"):

            # Lookup book info
            isbn = request.form.get("details")
            volumes = lookup(isbn)
            comments = db.execute("SELECT user_id, comment FROM comments WHERE isbn = ?", isbn)

            # If successful, display book info
            return render_template("info.html", title=volumes["title"], authors=volumes["authors"], cover=volumes["cover"], description=volumes["description"], isbn=isbn,comments=comments)

@app.route('/recommend')
@login_required
def get_recommendations():
    # Get the user's ID
    user_id = session.get("user_id")

    # Fetch books rated highly by the user (e.g., ratings greater than 4)
    high_rated_books = db.execute("SELECT DISTINCT isbn FROM rating WHERE username = ? AND rating > 4", user_id)

    # Extract the ISBNs of highly rated books into a list (Remove replicas)
    highly_rated_isbns = [book['isbn'] for book in high_rated_books]

    recommendations = []

    for isbn in highly_rated_isbns:
        # For each highly rated book, fetch other books that have similar ratings
        similar_rated_books = db.execute("SELECT DISTINCT isbn FROM rating WHERE isbn != ? AND username "
                                         "IN (SELECT username FROM rating WHERE isbn = ? AND rating > 4)", isbn, isbn)

        # Extract the ISBNs of similar rated books into a list
        similar_rated_isbns = [book['isbn'] for book in similar_rated_books]

        # Add the similar rated books to recommendations if not already rated by the user
        for similar_isbn in similar_rated_isbns:
            if similar_isbn not in highly_rated_isbns:
                recommendations.append(similar_isbn)

    # Remove duplicate ISBNs from the recommendations
    unique_recommendations = list(set(recommendations))
    print(unique_recommendations)

    # Limit the number of recommendations, for example, top 5 recommendations
    top_recommendations = unique_recommendations[:5]
    print(top_recommendations)

    # Fetch book details for the recommended ISBNs
    recommended_books = [lookup(isbn) for isbn in top_recommendations]

    # return render_template("recommendations.html", recommended_books=recommended_books)

@app.route('/rate_book', methods=['POST'])
def rate_book():
    data = request.get_json()
    isbn = data.get('isbn')
    userid = data.get('username')
    rating = data.get('rating')

    # Check if a record with the given ISBN and username already exists
    existing_record =db.execute("SELECT * FROM rating WHERE isbn = ? AND username = ?", isbn, userid)

    if existing_record:
        # Update the rating for the existing record
        db.execute("UPDATE rating SET rating = ? WHERE isbn = ? AND username = ?", rating, isbn, userid)
        return jsonify({'message': 'Rating updated'})
    else:
        # Add a new record with ISBN, username, and rating
        db.execute("INSERT INTO rating (isbn, username, rating) VALUES (?, ?, ?)", isbn, userid, rating)
        return jsonify({'message': 'New rating added'})

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    try:
        book_isbn = request.form.get('isbn')  # Assuming you pass the ISBN in the form
        user_id = session.get("user_id")
        comment = request.form.get('new_comment')

        # Insert the comment into the database
        db.execute("INSERT INTO comments (user_id, isbn, comment) VALUES (?, ?, ?)", user_id, book_isbn, comment)

        response_data = {
            "success": True,
            "message": "Comment submitted successfully"
        }
    except Exception as e:
        response_data = {
            "success": False,
            "message": str(e)
        }

    return jsonify(response_data)


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