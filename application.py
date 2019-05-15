import os
import requests

from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variables
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
if not os.getenv('GOODREADS_KEY'):
    raise RuntimeError("Goodreads API Key not found")

# Add Goodreads API Key
GoodreadsKey = os.getenv('GOODREADS_KEY')

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        newusername = request.form.get("newusername")
        newpassword = request.form.get("newpassword")
        try:
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                    {"username": newusername, "password": newpassword})
            db.commit()
            return render_template("login.html", message="Registration Successful, Please Login")
        except ValueError:
            render_template("error.html", message="Registration Unsuccessful")
    if request.method == "GET":
        if session:
            return render_template("home.html", username = session["user_id"][1])
        else:
            return render_template("login.html", message="Please Login")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/home", methods=["GET","POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT * FROM users WHERE username = :username AND password = :password",
        {"username": username, "password": password}).fetchone()
        if user:
            session["user_id"] = user
        else:
            return render_template("error.html", message="Login Unsuccessful")
    if session:
        return render_template("home.html", username = session["user_id"][1])
    else:
        return render_template("login.html", message="Please Login")

@app.route("/logout", methods = ["GET"])
def logout():
    session.clear()
    return render_template("login.html", message="Please Login")

@app.route("/books", methods=["POST"])
def books():
    identifier = request.form.get("input")
    books = db.execute("SELECT * FROM books WHERE title LIKE :input OR author LIKE :input OR isbn LIKE :input",
    {"input": '%'+ identifier +'%'}).fetchall()
    if books:
        return render_template('books.html', books=books)
    else:
        return render_template('error.html', message ="Book not found"),404


@app.route("/books/<string:isbn>", methods=["GET","POST"])
def book(isbn):
    if request.method == "POST":
        if db.execute("SELECT * FROM reviews WHERE isbn = :isbn AND user_id = :user_id", {"isbn": isbn, "user_id":session["user_id"][0]}).fetchone():
            return render_template('error.html', message = "Already Reviewed this Book")
        review_score = request.form.get("review_score")
        review = request.form.get("review")
        try:
            db.execute("INSERT INTO reviews (user_id, isbn, review_score, review) VALUES (:user_id, :isbn, :review_score, :review)",
            {"user_id":session["user_id"][0], "isbn": isbn, "review_score": review_score, "review": review})
            db.commit()
        except:
            return render_template('error.html', message = "Score must be between 1-5")
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    reviews = db.execute("SELECT * FROM reviews LEFT JOIN users ON reviews.user_id = users.id WHERE isbn =:isbn", {"isbn": isbn})
<<<<<<< HEAD
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "Eei1Pig7Rov3f6dMWX9A", "isbns": isbn})
=======
    # Call to Goodreads API
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": GoodreadsKey, "isbns": isbn})
>>>>>>> e0aa12a... Initial Commit
    goodreadsData = [res.json()['books'][0]['average_rating'], res.json()['books'][0]['work_ratings_count']]
    return render_template('book.html', book = book, reviews = reviews, goodreads = goodreadsData)

@app.route("/api/<string:isbn>", methods = ["GET"])
def api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn =:isbn",{"isbn": isbn}).fetchone()
    if book:
        reviews = db.execute("SELECT COUNT(review_score), CAST(AVG(review_score) AS FLOAT) FROM reviews WHERE isbn =:isbn", {"isbn": isbn}).fetchone()
        return jsonify({
            "title": book.title,
            "author": book.author,
            "publication_date": book.year,
            "isbn": book.isbn,
            "review_count": reviews[0],
            "review_average": reviews[1]
            })
    else:
        return jsonify({"error": "Book not found"}), 404
