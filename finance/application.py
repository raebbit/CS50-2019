import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, abort
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    cash0 = db.execute("SELECT cash FROM users WHERE id = :id",
                       id=session.get("user_id"))
    cash = usd(cash0[0]["cash"])

    stocks = db.execute("SELECT name, price, symbol, SUM(shares) FROM stocks WHERE user_id = :user_id GROUP BY symbol HAVING SUM(shares) > 0",
                        user_id=session.get("user_id"))

    # Total stock value
    totalval = 0
    for c in stocks:
        eachval = c["price"] * c["SUM(shares)"]
        totalval = totalval + eachval

    total = usd(cash0[0]["cash"] + totalval)

    return render_template("index.html", cash=cash, stocks=stocks, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check if the user's input is valid
        if not request.form.get("symbol"):
            return apology("Missing symbol", 400)
        elif not request.form.get("shares"):
            return apology("Missing shares", 400)
        elif request.form.get("shares").isnumeric() == False:
            return apology("Share must be a number", 400)
        elif int(request.form.get("shares")) < 0:
            return apology("Share must be positive", 400)
        elif float(request.form.get("shares")).is_integer() == False:
            return apology("Share must be integer", 400)

        # Check if the symbol does not exist
        quoted = lookup(request.form.get("symbol"))
        if not quoted:
            return apology("Invalid symbol", 400)

        # Query database to select how much cash the user has
        cash0 = db.execute("SELECT cash FROM users WHERE id = :id",
                           id=session.get("user_id"))
        cash = float(cash0[0]["cash"])

        # Check if the user can afford the stock
        stock_wannabuy = quoted["price"] * float(request.form.get("shares"))
        affordability = cash - stock_wannabuy
        if affordability < 0:
            return apology("You can't afford the stock!", 400)
        else:
            # Update cash and add stocks to user's history
            db.execute("UPDATE users SET cash = :cash WHERE id = :id",
                       cash=affordability, id=session.get("user_id"))
            db.execute("INSERT INTO stocks (user_id, name, price, shares, symbol) VALUES (:user_id, :name, :price, :shares, :symbol)",
                       user_id=session["user_id"], name=quoted["name"], price=quoted["price"], shares=request.form.get("shares"),
                       symbol=quoted["symbol"])

            # Show portfolio
            flash("You bought the stock!")
            return redirect("/")

    # User reached route via GET
    else:
        return render_template("buy.html")


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


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stocks = db.execute("SELECT * FROM stocks WHERE user_id = :user_id",
                        user_id=session.get("user_id"))

    return render_template("history.html", stocks=stocks)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol is submitted
        if not request.form.get("symbol"):
            return apology("Missing symbol", 400)

        quoted = lookup(request.form.get("symbol"))
        if not quoted:
            return apology("Invalid symbol", 400)

        # Show the stock quote
        else:
            price = usd(quoted["price"])
            return render_template("quoted.html", name=quoted["name"], price=price, symbol=quoted["symbol"])

    # User reached route via GET
    else:
        return render_template("quote.html")


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

        else:

            # Hash the password
            hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            # Add user to database
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                       username=request.form.get("username"), hash=hash)

            # login automatically
            login()

            return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure the symbol is submitted
        if not request.form.get("symbol"):
            return apology("Please select symbol", 400)

        # Ensure the share is submitted
        if not request.form.get("shares"):
            return apology("Missing shares", 400)

        # Apology if the user does not own any shares of the stock
        shares0 = db.execute("SELECT shares FROM stocks WHERE user_id = :user_id AND symbol = :symbol",
                             user_id=session.get("user_id"), symbol=request.form.get("symbol"))
        shares = shares0[0]["shares"]

        if not shares:
            return apology("You don't own any shares", 400)

        # Apology if user does not own enough shares to sell
        shares_sell = int(request.form.get("shares"))
        if shares_sell > shares:
            return apology("Too many shares", 400)

        quoted = lookup(request.form.get("symbol"))

        # Log sale as a negative quantity
        db.execute("INSERT INTO stocks (user_id, name, price, shares, symbol) VALUES (:user_id, :name, :price, :shares, :symbol)",
                   user_id=session["user_id"], name=quoted["name"], price=quoted["price"], shares=-shares_sell, symbol=quoted["symbol"])

        # Update cash
        cash0 = db.execute("SELECT cash FROM users WHERE id = :id",
                           id=session.get("user_id"))
        cash = float(cash0[0]["cash"])
        stock_wannasell = quoted["price"] * float(request.form.get("shares"))
        cash_new = cash + stock_wannasell
        db.execute("UPDATE users SET cash = :cash WHERE id = :id",
                   cash=cash_new, id=session.get("user_id"))

        flash("Sold!")
        return redirect("/")

    # User reached route via GET
    else:
        # Display symbols that user have
        symbols = db.execute("SELECT symbol FROM stocks WHERE user_id = :user_id GROUP BY symbol HAVING SUM(shares) > 0",
                             user_id=session.get("user_id"))
        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
