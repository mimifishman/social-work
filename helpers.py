import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from geopy.geocoders import Nominatim
import sqlite3


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

def company_required(f):
    """
    Decorate routes to require company.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("company_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function 

# format USD
def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


# get dict from sqlite row
def dict_from_row(row):
    return dict(zip(row.keys(), row))       

# get the longitude and lalitude of a location
def geo(userid):  
    #connect to database
    con = sqlite3.connect("socialwork.db",check_same_thread=False)  
    with con:
        # create dict table with names
        con.row_factory = sqlite3.Row
        cur = con.cursor()  

    #get the address of the user
    cur.execute("SELECT id, address1 || ', ' || city || ', ' || zipcode address FROM user WHERE id = ? ",[userid])  
    user = cur.fetchone()         
    # get the address geo location
    geolocator = Nominatim(user_agent="MyApp")
    if geolocator.geocode(user["address"]):
        location = geolocator.geocode(user["address"])         
        lat = location.latitude
        long = location.longitude

        # check if the user exists in the user table
        cur.execute("SELECT userid FROM geo_location where userid = ?",[userid])  
        geo = cur.fetchone()

        # insert or update the geo table 
        if geo == None:
            cur.execute("INSERT INTO  geo_location values(NULL, ? ,?, ?)",[ userid, lat, long] )
            con.commit()
            con.close
        else:
            cur.execute("UPDATE geo_location SET latitude = ?, longitude = ? where userid = ?",[lat, long, userid] )
            con.commit()
            con.close
