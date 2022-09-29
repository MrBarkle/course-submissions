import os
import datetime
import sys

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, clean, convert_date, compare_date


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
app.jinja_env.filters["clean"] = clean
app.jinja_env.filters["convert_date"] = convert_date
app.jinja_env.filters["compare_date"] = compare_date


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///application.db")


@app.route("/")
def index(arg=None):
    """Display main user page"""

    # If user is not logged in, display welcome page
    if session.get("user_id") is None:

        return render_template("welcome.html")

    # If user is logged in, display their tab information
    else:

        # Get current user id
        user_id = session["user_id"]

        # Check how many notebooks current user has
        nb_total = int(db.execute("SELECT COUNT(number) AS count FROM notebooks WHERE user_id = ?", user_id)[0]["count"])

        # Check how many experiments current user has
        exp_total = int(db.execute("SELECT COUNT(exp_number) AS count FROM experiments WHERE user_id = ?", user_id)[0]["count"])

        # Get notebook info for user + associated partners from experiements table
        notebooks = db.execute(
            "SELECT number, course, section, semester, year, instructor, last_active, base_hex, border, text, header, disabled, enabled, button, rgb, colors.id AS id, \
            GROUP_CONCAT(partners, ', ') AS partners FROM notebooks LEFT JOIN experiments ON notebooks.user_id = experiments.user_id AND \
            notebooks.number = experiments.notebook_no JOIN colors ON notebooks.color_id = colors.id WHERE notebooks.user_id = ? GROUP BY notebooks.number", user_id)

        # Get all base color values and associated data
        themes = db.execute("SELECT * from colors")

        # Get profile info for user
        profile = db.execute("SELECT first_name, last_name FROM profiles WHERE user_id = ?", user_id)[0]

        if arg == None:
            # Get experiment info for user
            experiments = db.execute(
                "SELECT notebook_no, topic, date_started, date_modified, exp_number, partners FROM experiments WHERE user_id = ?", user_id)
        else:
            experiments = arg

        return render_template("index.html", nb_total=nb_total, exp_total=exp_total, notebooks=notebooks, profile=profile, experiments=experiments, themes=themes)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for email
        email = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email").lower())

        # Ensure email exists and password is correct
        if len(email) != 1 or not check_password_hash(email[0]["hash"], request.form.get("password")):
            return render_template("login.html", alert=1)

        # Remember which user has logged in
        session["user_id"] = email[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect or back/forward navigation)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/signup", methods=["POST"])
def signup():
    """Sign up for a user account"""

    # User reached route via POST (as by submitting a form via POST)

    # Gather required variables
    first_name = request.form.get("first_name").lower()
    last_name = request.form.get("last_name").lower()
    email = request.form.get("email").lower()
    pwd = request.form.get("password")

    # Handle empty form inputs
    empty = 'NULL'

    # Handle optional variables
    address = request.form.get("address")
    if address == '' or address == None:
        address = empty
    city = request.form.get("city")
    if city == '' or city == None:
        city = empty
    state = request.form.get("state")
    if state == '' or state == None:
        state = empty
    zipcode = request.form.get("zip")
    if zipcode == '' or zipcode == None:
        zipcode = empty
    phone = request.form.get("phone")
    if phone == '' or phone == None:
        phone = empty
    network = request.form.get("network")
    if network == '' or network == None:
        network = empty

    # Query database for given user by unique email
    new_user = db.execute("SELECT * FROM users WHERE email = ?", email)

    # Ensure user does not exist
    if len(new_user) != 0:
        return render_template("login.html", alert=2)

    # Generate password hash
    pwd_hash = generate_password_hash(pwd)

    # Set email and password in database
    db.execute("INSERT INTO 'users' ('email', 'hash') VALUES(?, ?)", email, pwd_hash)

    # Query database for new user's id
    user_id = db.execute("SELECT id FROM users WHERE email = ?", email)[0]["id"]

    # Set other profile attributes if provided
    db.execute("INSERT INTO 'profiles' ('user_id', 'first_name', 'last_name', 'address', 'city', 'state', 'zip', 'phone', 'network_id') VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
               user_id, first_name, last_name, address, city, state, zipcode, phone, network)

    # Auto log user in on sign up
    session["user_id"] = user_id

    # Redirect user to home page.
    return redirect("/")


@app.route("/profile", methods=["GET"])
@login_required
def profile():
    """View user's profile"""

    # User reached route via GET (as by clicking a link or via redirect or back/forward navigation)

    # Get current user id
    user_id = session["user_id"]

    name = db.execute("SELECT first_name, last_name FROM profiles WHERE user_id = ?", user_id)[0]

    # Render profile page
    return render_template("profile.html", alert=1, name=name)


@app.route("/experiment", methods=["POST", "GET"])
@login_required
def experiment():
    """Start a new laboratory experiment or visit an old one"""

    # Select all from periodic table data
    pt = db.execute("SELECT * FROM periodic")

    # Get current user id
    user_id = session["user_id"]

    # Get profile info for user
    profile = db.execute("SELECT first_name, last_name FROM profiles WHERE user_id = ?", user_id)[0]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Handle empty form inputs
        empty = 'NULL'

        # Get current local date and time
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Gather required variables
        topic = request.form.get("topic")
        number = request.form.get("notebook_no")

        # Get associated color data
        color = db.execute(
            "SELECT colors.id AS id, base_hex, text, button, border, header, disabled, enabled, rgb FROM colors JOIN notebooks ON colors.id = notebooks.color_id WHERE notebooks.user_id = ? AND notebooks.number = ?",
            user_id, number)[0]

        # Gather potential variables
        partners = request.form.get("partners")
        if partners == '' or partners == None:
            partners = empty
        desk = request.form.get("desk_number")
        if desk == '' or desk == None:
            desk = empty

        # Get current experiment count (after addition of new experiement) for this notebook
        curr_number = db.execute(
            "SELECT COUNT(exp_number) AS count FROM experiments WHERE notebook_no IN (SELECT number FROM notebooks WHERE user_id = ? AND number = ?) AND user_id = ?", user_id, number, user_id)[0]["count"] + 1

        # Set other experiment attributes if provided
        db.execute("INSERT INTO 'experiments' ('user_id', 'notebook_no', 'topic', 'date_started', 'date_modified', 'exp_number', 'desk_number', 'partners', 'content') VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   user_id, number, topic, date, date, curr_number, desk, partners, empty)

        # Get experiment and notebook attributes as dictionary
        exp = db.execute(
            "SELECT topic, date_started, partners, desk_number, course, section, notebook_no, exp_number, content FROM experiments JOIN notebooks ON experiments.notebook_no = notebooks.number WHERE exp_number = ? AND notebook_no = ? AND experiments.user_id = ?", curr_number, number, user_id)[0]

        # Get previously active notebook number
        prev_active = db.execute("SELECT number FROM notebooks WHERE user_id = ? and last_active = ?", user_id, 1)

        # Skip if no previously active notebooks (prev active was deleted)
        if prev_active != []:
            # Set previously active notebook's status to 0 for False
            db.execute("UPDATE notebooks SET last_active = ? WHERE user_id = ? AND number = ?",
                       0, user_id, prev_active[0]["number"])

        # Set current notebook's active status to 1 for True
        db.execute("UPDATE notebooks SET last_active = ? WHERE user_id = ? AND number = ?", 1, user_id, number)

        # Redirect user to new experiment page
        return render_template("experiment.html", pt=pt, exp=exp, profile=profile, color=color)

    # User reached route via GET (as by clicking a link or via redirect or back/forward navigation)
    else:

        # Get experiment number
        exp_no = request.args.get("exp")

        # Get notebook number
        ntb_no = request.args.get("nb")

        # Get associated color data
        color = db.execute(
            "SELECT colors.id, base_hex, text, button, border, header, disabled, enabled, rgb FROM colors JOIN notebooks ON colors.id = notebooks.color_id WHERE notebooks.user_id = ? AND notebooks.number = ?",
            user_id, ntb_no)[0]

        # Get experiment and notebook attributes as dictionary
        exp = db.execute(
            "SELECT topic, date_started, partners, desk_number, course, section, notebook_no, exp_number, content FROM experiments JOIN notebooks ON experiments.notebook_no = notebooks.number WHERE exp_number = ? AND notebook_no = ? AND experiments.user_id = ?", exp_no, ntb_no, user_id)[0]

        # Redirect user to existing experiment page
        return render_template("experiment.html", pt=pt, exp=exp, profile=profile, color=color)


@app.route("/delete_experiment", methods=["POST"])
@login_required
def delete_experiment():
    """Delete desired experiment"""

    # User reached route via POST (as by submitting a form via POST)

    # Get current user id
    user_id = session["user_id"]

    # Get experiment to be deleted
    exp_number = int(request.form.get("exp_number"))

    # Get notebook number to which experiment belongs
    notebook = int(request.form.get("notebook_no"))

    # Get current experiment total (before deletion)
    curr_exp_total = db.execute(
        "SELECT COUNT(user_id) as count FROM experiments WHERE user_id = ? and notebook_no = ?", user_id, notebook)[0]["count"]

    # Delete experiment and associated experimentData
    db.execute("DELETE FROM experiments WHERE user_id = ? AND exp_number = ? AND notebook_no = ?", user_id, exp_number, notebook)

    # Get previously active notebook number
    prev_active = db.execute("SELECT number FROM notebooks WHERE user_id = ? and last_active = ?", user_id, 1)

    # Skip if no previously active notebooks (prev active was deleted)
    if prev_active != []:
        # Set previously active notebook's status to 0 for False
        db.execute("UPDATE notebooks SET last_active = ? WHERE user_id = ? AND number = ?", 0, user_id, prev_active[0]["number"])

    # Set current notebook's active status to 1 for True
    db.execute("UPDATE notebooks SET last_active = ? WHERE user_id = ? and number = ?", 1, user_id, notebook)

    # Update number for remaining experiments listed after deletion
    for current in range(exp_number + 1, curr_exp_total + 1):
        db.execute("UPDATE experiments SET exp_number = ? WHERE user_id = ? AND exp_number = ?", (current - 1), user_id, current)

    # Redirect user to home page.
    return redirect("/")


@app.route("/update_exp_head", methods=["POST"])
@login_required
def update_exp_head():
    """ Update header for experiment and save any progress """

    # User reached route via POST (as by submitting a form via POST)

    # Handle empty form inputs
    empty = 'NULL'

    # Get current user id
    user_id = session["user_id"]

    # Gather potential variables
    topic = request.form.get("topic")
    if topic == '' or topic == None:
        topic = empty
    partners = request.form.get("partners")
    if partners == '' or partners == None:
        partners = empty
    desk = request.form.get("desk")
    if desk == '' or desk == None:
        desk = empty

    # Get additional hidden data
    exp = request.form.get("exp")
    number = request.form.get("number")
    content = request.form.get("content")

    # Get current local date and time
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update experiment attributes
    db.execute("UPDATE experiments SET topic = ?, partners = ?, desk_number = ?, content = ? , date_modified = ? WHERE user_id = ? AND notebook_no = ? AND exp_number = ?",
               topic, partners, desk, content, date, user_id, number, exp)

    # Redirect user to experiment page
    return redirect("/experiment?nb=" + number + "&exp=" + exp)


@app.route("/save_experiment", methods=["POST"])
@login_required
def save_experiment():
    """ Save experiment content to DB """

    # User reached route via POST (as by submitting a form via POST)

    # Get current user id
    user_id = session["user_id"]

    # Get content data and save point location
    exp = request.form.get("exp")
    number = request.form.get("number")
    content = request.form.get("content")

    # Get current local date and time
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update experiment content
    db.execute("UPDATE experiments SET content = ? , date_modified = ? WHERE user_id = ? AND notebook_no = ? AND exp_number = ?",
               content, date, user_id, number, exp)

    # Redirect user to experiment page
    return redirect("/experiment?nb=" + number + "&exp=" + exp)


@app.route("/notebook", methods=["POST"])
@login_required
def create_notebook():
    """ Create a new laboratory notebook """

    # User reached route via POST (as by submitting a form via POST)

    # Handle empty form inputs
    empty = 'NULL'

    # Get current user id
    user_id = session["user_id"]

    # Gather potential variables
    course = request.form.get("course")
    if course == '' or course == None:
        course = empty
    section = request.form.get("section")
    if section == '' or section == None:
        section = empty
    semester = request.form.get("semester")
    if semester == '' or semester == None:
        semester = empty
    year = request.form.get("year")
    if year == '' or year == None:
        year = empty
    instructor = request.form.get("instructor")
    if instructor == '' or instructor == None:
        instructor = empty

    # Get current notebook number
    curr_number = db.execute("SELECT COUNT(user_id) as count FROM notebooks WHERE user_id = ?", user_id)[0]["count"] + 1

    # Get previously active notebook number
    prev_active = db.execute("SELECT number FROM notebooks WHERE user_id = ? and last_active = ?", user_id, 1)

    # Skip if creating first notebook
    if prev_active != []:
        # Set previously active notebook's status to 0 for False
        db.execute("UPDATE notebooks SET last_active = ? WHERE user_id = ? AND number = ?", 0, user_id, prev_active[0]["number"])

    # Set other profile attributes if provided. Set 'last_active' status to 1 for True. Set color_id default to 0
    db.execute("INSERT INTO 'notebooks' ('user_id', 'color_id', 'number', 'course', 'section', 'semester', 'instructor', 'year', 'last_active') VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
               user_id, 0, curr_number, course, section, semester, instructor, year, 1)

    # Redirect user to home page.
    return redirect("/")


@app.route("/delete_notebook", methods=["POST"])
@login_required
def delete_notebook():
    """Delete desired notebook"""

    # User reached route via POST (as by submitting a form via POST)

    # Get current user id
    user_id = session["user_id"]

    # Get notebook to be deleted
    notebook = int(request.form.get("notebook_no"))

    # Get previously active notebook number
    prev_active = db.execute("SELECT number FROM notebooks WHERE user_id = ? and last_active = ?", user_id, 1)

    # Get current notebook total (before deletion)
    curr_total = db.execute("SELECT COUNT(user_id) as count FROM notebooks WHERE user_id = ?", user_id)[0]["count"]

    # Delete notebook and all associated experiments
    db.execute("DELETE FROM experiments WHERE user_id = ? and notebook_no = ?", user_id, notebook)
    db.execute("DELETE FROM notebooks WHERE user_id = ? AND number = ? ", user_id, notebook)

    # Update number for remaining notebooks listed after deletion
    for current in range(notebook + 1, curr_total + 1):
        db.execute("UPDATE notebooks SET number = ? WHERE user_id = ? AND number = ?", (current - 1), user_id, current)

    # Check to see if notebook that was deleted was also the previously active notebook
    if notebook == prev_active[0]["number"]:
        # If it was prev active and now deleted, if there is remaining notebooks
        if (curr_total - 1) > 0:
            # Update last of remaining notebooks to active status
            db.execute("UPDATE notebooks SET last_active = ? WHERE user_id = ? AND number = ?", 1, user_id, (curr_total - 1))

    # Redirect user to home page.
    return redirect("/")


@app.route("/update_notebook", methods=["POST"])
@login_required
def update_notebook():
    """Update desired notebook fields"""

    # User reached route via POST (as by submitting a form via POST)

    # Get current user id
    user_id = session["user_id"]

    # Get submission variables that can be altered
    color = request.form.get("last_clicked")
    notebook = request.form.get("number")
    course = request.form.get("course")
    section = request.form.get("section")
    semester = request.form.get("semester")
    year = request.form.get("year")
    instructor = request.form.get("instructor")

    # Get previously active notebook number
    prev_active = db.execute("SELECT number FROM notebooks WHERE user_id = ? and last_active = ?", user_id, 1)

    # Set previously active notebook's status to 0 for False
    db.execute("UPDATE notebooks SET last_active = ? WHERE user_id = ? AND number = ?", 0, user_id, prev_active[0]["number"])

    # Update all and set updated notebook's active status to 1 for True
    db.execute("UPDATE notebooks SET color_id = ?, course = ?, section = ?, semester = ?, year = ?, instructor = ?, last_active = ? WHERE user_id = ? and number = ?",
               color, course, section, semester, year, instructor, 1, user_id, notebook)

    # Redirect user to home page.
    return redirect("/")


@app.route("/", methods=["POST"])
@login_required
def sort_table():
    """Sort experiments table"""

    # User reached route via POST (as by submitting a form via POST)

    # Get current user id
    user_id = session["user_id"]

    # Get notebook number for table being sorted
    number = request.form.get("number")

    # Sort by title
    if request.form.get("title"):
        # Get sorted experiment info for user
        experiments = db.execute(
            "SELECT notebook_no, topic, date_started, date_modified, exp_number, desk_number, partners FROM experiments WHERE user_id = ? ORDER BY topic", user_id)

    # Sort by date experiment was started
    elif request.form.get("start"):
        # Get sorted experiment info for user
        experiments = db.execute(
            "SELECT notebook_no, topic, date_started, date_modified, exp_number, desk_number, partners FROM experiments WHERE user_id = ? ORDER BY date_started", user_id)

    # Sort by last modified
    elif request.form.get("modified"):
        # Get sorted experiment info for user
        experiments = db.execute(
            "SELECT notebook_no, topic, date_started, date_modified, exp_number, desk_number, partners FROM experiments WHERE user_id = ? ORDER BY date_modified", user_id)

    # Get previously active notebook number
    prev_active = db.execute("SELECT number FROM notebooks WHERE user_id = ? and last_active = ?", user_id, 1)

    # Skip if no previously active notebooks (prev active was deleted)
    if prev_active != []:
        # Set previously active notebook's status to 0 for False
        db.execute("UPDATE notebooks SET last_active = ? WHERE user_id = ? AND number = ?", 0, user_id, prev_active[0]["number"])

    # Set current notebook's active status to 1 for True
    db.execute("UPDATE notebooks SET last_active = ? WHERE user_id = ? and number = ?", 1, user_id, number)

    return index(experiments)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
