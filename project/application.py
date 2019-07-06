import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from random import choice

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///wordnote.db")


@app.route("/")
@login_required
def index():
    """Show how to use the website and the results of quiz"""
    
    # ID card
    card0 = db.execute("SELECT username, first_day FROM users WHERE id = :user_id",
                       user_id=session["user_id"])
    card = card0[0]
    
    # Display the result on `index.html`
    corr_rate0 = db.execute("SELECT quiz_total, quiz_corr FROM users WHERE id = :user_id",
                            user_id=session["user_id"])
    corr_rate = corr_rate0[0]
    
    if corr_rate["quiz_total"] == 0:
        correctness = 0
    else:
        correctness = int((corr_rate["quiz_corr"]/corr_rate["quiz_total"])*100)

    return render_template("index.html", corr_rate=corr_rate, card=card, correctness=correctness)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Search the meaning of words"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check if the user's input is not blank
        if not request.form.get("word"):
            return apology("Missing Word", 400)
        
        # When word is submitted, show meaning.html
        return render_template("meaning.html", word=request.form.get("word"))

    # User reached route via GET
    else:
        return render_template("search.html")


@app.route("/meaning", methods=["GET", "POST"])
@login_required
def makenote():
    """Make the user create wordnote in their own words"""
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        sameword = db.execute("SELECT word FROM words WHERE user_id = :user_id AND word = :word",
                              user_id=session["user_id"], word=request.form.get("word"))
        
        # Check if the inputs are not blank
        if not request.form.get("word"):
            return apology("Missing word", 400)
        elif sameword:
            return apology("Word already exist in the note", 400)
        elif not request.form.get("meaning"):
            return apology("You must write the meaning", 400)
            
        # Add note to database
        else:
            db.execute("INSERT INTO words (word, meaning, user_id) VALUES (:word, :meaning, :user_id)",
                       word=request.form.get("word"), meaning=request.form.get("meaning"), user_id=session["user_id"])
                    
            flash("You saved new word in your note! You'll see it in your Note!")
            return redirect("/")
            
    # User reached route via GET
    else:
        return render_template("meaning.html")
        
        
@app.route("/mynote", methods=["GET", "POST"])
@login_required
def mynote():
    """Show the user's wordnote"""
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
    
        # Delete selected table row
        if request.form.get("delete"):
            db.execute("DELETE FROM words WHERE id = :id", id=request.form.get("delete"))
            
            words = db.execute("SELECT * FROM words WHERE user_id = :user_id", user_id=session["user_id"])
            
            return render_template("mynote.html", words=words)
            
    else:
        words = db.execute("SELECT * FROM words WHERE user_id = :user_id",
                           user_id=session.get("user_id"))
        return render_template("mynote.html", words=words)


@app.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    """make a quiz for the user"""
        
    # User reached route via GET
    if request.method == "GET":
        
        # Make a list of words
        id0 = db.execute("SELECT id FROM words WHERE user_id = :user_id", user_id=session["user_id"])
        
        # no quiz if no words
        if not id0:
            return apology("Your note is empty", 400)
    
        else:
            # Choose one randomly and a quiz. ex) id0 = [{'id':18}, {'id': 19}, {'id':21}]
            quiz_id = choice(id0)["id"]
        
            quiz0 = db.execute("SELECT * FROM words WHERE id = :id", id=quiz_id)
            # quiz0 = [{  }]
            quiz = quiz0[0]
            
            return render_template("quiz.html", quiz=quiz)
            
    # User reached route via POST (as by submitting a form via POST)
    else:
        
        # Ensure the answer is submitted
        if not request.form.get("answer"):
            return apology("submit the answer!", 400)
        
        # If the answer is wrong or right, show the result(index.html)
        else:
            
            if request.form.get("answer") != request.form.get("checking"):
            
                # Update the number of total quiz
                db.execute("UPDATE users SET quiz_total = quiz_total + 1 WHERE id = :user_id",
                           user_id=session["user_id"])
                        
                flash("Quiz Result : Awwwww :(  Wrong Answer!!!!!!")
                return redirect("/")
            
            else:
            
                # Update the number of total quiz
                db.execute("UPDATE users SET quiz_total = quiz_total + 1 WHERE id = :user_id",
                           user_id=session["user_id"])
                # Update the number of the correct answers
                db.execute("UPDATE users SET quiz_corr = quiz_corr + 1 WHERE id = :user_id",
                           user_id=session["user_id"])
                            
                flash("Quiz Result : You are correct!!!!!!!")
                return redirect("/")
        
    
@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    samename = db.execute("SELECT username FROM users WHERE username = :username", username=username)

    # Ensure the username is available (return in JSON format)
    if len(username) < 1:
        return jsonify(False)
    elif len(username) > 0 and not samename:
        return jsonify(True)
    else:
        return jsonify(False)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Logged in!")
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
    flash("Logged out!")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # via POST request
    if request.method == "POST":

        # Query database for checking the username is already taken
        samename = db.execute("SELECT username FROM users WHERE username = :username",
                              username=request.form.get("username"))

        # proper username from user
        if not request.form.get("username"):
            return apology("Missing username!", 400)
        elif samename:
            return apology("The username already exist", 400)

        # Check if the password is valid
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Missing password!", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("The passwords do not match!", 400)
        elif len(request.form.get("password")) < 4:
            return apology("Password must be longer than 3 letters", 400)
        else:

            # Hash the password
            hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            # Add user to database
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                       username=request.form.get("username"), hash=hash)

            # login automatically
            login()

            return redirect("/")

    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
