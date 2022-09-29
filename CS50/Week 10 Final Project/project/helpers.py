import os
import datetime
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    '''Render message as an apology to user.'''
    return render_template("apology.html", top=code, bottom=message), code


def login_required(f):
    '''
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def clean(l):
    '''
    Takes a NoneType that represents a list of names, converts it to a string
    and splits it at commas, removing any duplicate words as well as white space
    or Null types (if other names present) then returns it as a string of
    unique comma separated names.

    This also bypasses case and then capitalizes each space separated word.
    '''

    words = sorted(set([word.strip().lower().title() for word in str(l).split(',')]))
    length = len(words)
    if "Null" in words and length > 1:
        words.remove("Null")

    elif "Null" in words and length == 1:
        words.remove("Null")
        words.append("None")

    return ", ".join(words)


def convert_date(date):
    ''' Convert datetime format to desired output of Jun 3, 2021'''

    date, time = str(date).split(" ")
    convert = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%b %-d %Y')
    return convert


def compare_date(date):
    ''' Compare two datetimes '''

    # Gather current datetime
    dt_now = datetime.datetime.now()

    # Get datetime of 'last modified'
    dt_then = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Compare time elapsed
    elapsed = dt_now - dt_then

    # Get time elapsed in seconds
    seconds = elapsed.total_seconds()

    if int(seconds) < 60:
        if int(seconds) == 1:
            return str(int(seconds)) + " second ago"
        else:
            return str(int(seconds)) + " seconds ago"

    # Get time elapsed in minutes
    minutes = int(divmod(seconds, 60)[0])

    if int(minutes) < 60:
        if int(minutes) == 1:
            return str(minutes) + " minute ago"
        else:
            return str(minutes) + " minutes ago"

    # Get time elapsed in hours
    hours = int(divmod(seconds, 3600)[0])

    if int(hours) < 24:
        if int(hours) == 1:
            return str(hours) + " hour ago"
        else:
            return str(hours) + " hours ago"

    # Get time elapsed in days
    days = elapsed.days

    if int(days) < 30:
        if int(days) == 1:
            return str(days) + " day ago"
        else:
            return str(days) + " days ago"

    # Return converted date
    return convert_date(date)
