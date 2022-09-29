import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():

    portfolio = db.execute(
        "SELECT symbol, name, SUM(shares) AS shares, SUM(price) AS price, SUM(shares * price) AS totals FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("index.html", portfolio=portfolio,  cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Gather variables
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # Ensure symbol and shares amount are input
        if not shares or not symbol:
            return apology("must provide valid stock symbol and amount of shares to buy", 400)

        # Ensure symbol was input
        elif not symbol:
            return apology("must provide stock symbol", 400)

        # Ensure symbol was valid
        elif lookup(symbol) == None:
            return apology("must provide valid stock symbol", 400)

        try:
            # Ensure amount is positive and numeric:
            if float(shares) <= 0 or not shares.isnumeric():
                return apology("must be positive integer", 400)
        except:
            return apology("must input numeric value")

        # Lookup name of company
        name = str(lookup(symbol)["name"])

        # Lookup price of shares
        price = float(lookup(symbol)["price"])

        # Check how much cash the user has
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        # Make sure the user has enough money to purchase shares
        purchase = price * float(shares)
        if not purchase < cash:
            return apology(f"Cannot afford {shares} shares of {symbol}.")

        # Make purchase
        else:
            # Insert transaction into 'transaction' table
            db.execute("INSERT INTO 'transactions' ('user_id', 'symbol', 'name', 'shares', 'price', 'transacted') VALUES(?, ?, ?, ?, ?, DateTime('now'))",
                       session["user_id"], symbol, name, shares, price)
            # Update cash totals in 'users' table
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", purchase, session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():

    # Query for transaction history
    history = db.execute("SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = ?", session["user_id"])

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Gather variables
        username = request.form.get("username")
        pwd = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not pwd:
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], pwd):
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


@app.route("/reset", methods=["GET", "POST"])
def reset():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Gather variables
        pwd = request.form.get("new")
        pwd_hash = generate_password_hash(pwd)

        # Ensure username and password were set
        if not pwd:
            return apology("must provide all fields", 403)

        # Update user with new password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", pwd_hash, session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("reset.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Look up user input symbol
        quoted = lookup(request.form.get("symbol"))

        # Ensure valididty
        if quoted == None:
            return apology("Invalid stock symbol", 400)

        # Valid symbol, get quote
        else:
            return render_template("quoted.html", quoted=quoted)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Gather variables
        username = request.form.get("username")
        pwd = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username and password were set
        if not username and not pwd:
            return apology("must provide a username and password", 400)

        # Ensure username was set
        elif not username:
            return apology("must provide a username", 400)

        # Ensure password was set
        elif not pwd:
            return apology("must provide a password", 400)

        # Ensure password was confirmed
        elif not confirmation:
            return apology("must confirm password", 400)

        # Ensure password and confirmation are the same
        elif not confirmation == pwd:
            return apology("confirmation and password do not match", 400)

        # Query database for given username
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username does not exist
        if len(user) != 0:
            return apology("username already exists", 400)

        # Generate password hash
        pwd_hash = generate_password_hash(pwd)
        # Set username and password in database
        db.execute("INSERT INTO 'users' ('username', 'hash') VALUES(?, ?)", username, pwd_hash)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Gather variables
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        amount = db.execute("SELECT SUM(shares) AS amount FROM transactions WHERE user_id IN (SELECT id FROM users WHERE id = ?) AND symbol = ?",
                            session["user_id"], symbol)[0]["amount"]

        # Ensure user has desired stocks
        if not symbol:
            if amount == None:
                return apology(f"You do not have any shares of that type to sell.", 400)
            else:
                return apology("Failed to select stock", 400)

        # Ensure user can sell desired amount
        elif not shares or amount < int(shares):
            return apology(f"You do not own that many shares of {symbol} stock.", 400)
        else:
            # Lookup name of company
            name = str(lookup(symbol)["name"])

            # Lookup price of shares
            price = float(lookup(symbol)["price"])

            # Calculate how much the stocks sell for
            credit = price * float(shares)

            # Update cash balance in users
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", credit, session["user_id"])

            # Insert sale into transactions table
            db.execute("INSERT INTO 'transactions' ('user_id', 'symbol', 'name', 'shares', 'price', 'transacted') VALUES(?, ?, ?, (? * -1), ?, DateTime('now'))",
                       session["user_id"], symbol, name, shares, price)

        # Redirect user to home page
        return redirect("/")

     # User reached route via GET (as by clicking a link or via redirect)
    else:
        # provide list of avialable stocks with totals
        available = db.execute(
            "SELECT symbol, SUM(shares) as shares FROM transactions WHERE user_id IN (SELECT id FROM users WHERE id = ?) GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        return render_template("sell.html", available=available)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
