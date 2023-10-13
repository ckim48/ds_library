import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(isbn):
    """Look up volume info using isbn."""

    # Contact API
    try:
        # api_key = os.environ.get("API_KEY")
        url = f"https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote_plus(str(isbn))}+isbn"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        volumes = response.json()
        return {
            # String of title
            "title": volumes["items"][0]["volumeInfo"]["title"],
            # A list of author(s)
            "authors": volumes["items"][0]["volumeInfo"]["authors"],
            # String of cover image LINK
            "cover": volumes["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"],
            # String of description
            "description": volumes["items"][0]["volumeInfo"]["description"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def strOfAuthors(authors):
    """Return a list of authors as a string."""
    authorsStr = ""
    for author in authors:
        authorsStr += author + ", "
    return authorsStr