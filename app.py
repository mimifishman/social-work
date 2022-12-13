import os
from datetime import datetime, timedelta
import datetime
import sqlite3
from sqlite3.dbapi2 import Row
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from geopy.distance import geodesic
import logging


from helpers import apology, login_required, usd, company_required, dict_from_row, geo
from forms import CompanyRegistrationForm, EmployeeRegistrationForm, loginform,  CafeSignupForm, AccountUpdateForm, PasswordUpdateForm

# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True
    app.run(debug=True)   
        

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# set secret key for CSRF for Flask Forms
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#connect to database
con = sqlite3.connect("socialwork.db",check_same_thread=False)
with con:
    # create dict table with names
    con.row_factory = sqlite3.Row
    cur = con.cursor()  

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/companyregister", methods=["GET", "POST"])
def companyregister():
    form = CompanyRegistrationForm()
    
    # get a list of countries from the database 
    cur.execute("SELECT id,name FROM countries")
    countries = cur.fetchall()     
    form.country.choices = [( " ","Select" )] + [(country["id"],country["name"]) for country in countries]    
        
    #check if the form is valid
    if form.validate_on_submit():        
        # get the data from the forms
        fieldDict={}        
        for key in request.form.keys():
            fieldDict[key]= request.form.get(key)
            # app.logger.info(fieldDict)
        
        # check if the company exists
        cur.execute("SELECT company FROM company WHERE company = ? COLLATE NOCASE",[fieldDict["company"]] ) 
        cmp = cur.fetchone() 
        if not cmp == None:
            flash("Company already registered!")
            return render_template("companyregister.html",form=form,countries=countries)               
                
        # check if the email address exists
        cur.execute("SELECT id FROM user WHERE email = ? COLLATE NOCASE",[fieldDict["email"]] ) 
        email = cur.fetchone() 
        if not email == None:
            flash("Email address already registered!")
            return render_template("companyregister.html",form=form,countries=countries)                 
         
        #update the company table
        cur.execute("INSERT INTO company (typeid,company,timestamp) values(1,?,CURRENT_TIMESTAMP)",[fieldDict["company"]])           
        con.commit()
        cur.close
        
        # # get the company id
        cur.execute("SELECT id FROM company WHERE company = ?",[fieldDict["company"]] ) 
        company=cur.fetchone()
        session["company_id"] = company["id"]              

        # hash the password
        password=generate_password_hash(fieldDict["password"]) 
        
        # update the user table 
        cur.execute("INSERT INTO user values(null,1,?,?,?,?,?,?,?,?,?,?,?,?,0,1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)",
         [company["id"],fieldDict["firstname"],
         fieldDict["lastname"], fieldDict["phone"],  
         fieldDict["email"], fieldDict["address1"],  
         fieldDict["address2"], fieldDict["city"],  
         fieldDict["state"], fieldDict["zipcode"],  
         fieldDict["country"], password ])
        con.commit()
        cur.close                 

        # update the session user_id
        cur.execute("SELECT id FROM user WHERE email = ?",[fieldDict["email"]] ) 
        user=cur.fetchone()
        session["user_id"] = user["id"]
        userid = user["id"]
        #update the geo_location table
        geo(userid)

        return render_template("index.html")           
       
    return render_template("companyregister.html",form=form,countries=countries) 


@app.route("/employeeregister", methods=["GET", "POST"])
def employeeregister():
    form = EmployeeRegistrationForm() 
    
    # get a list of countries from the database 
    cur.execute("SELECT id,name FROM countries")
    countries = cur.fetchall()     
    form.country.choices = [( " ","Select" )] + [(country["id"],country["name"]) for country in countries]     

    # get a list of companies
    cur.execute("SELECT id, company FROM company where typeid = 1")
    companies = cur.fetchall() 
    form.company.choices = [( " ","Select" )] + [(company["id"],company["company"]) for company in companies]      
        
    #check if the form is valid
    if form.validate_on_submit():        
        # get the data from the forms
        fieldDict={}        
        for key in request.form.keys():
            fieldDict[key]= request.form.get(key)
            # app.logger.info(fieldDict)  

        # check if the email address exists
        cur.execute("SELECT id FROM user WHERE email = ? COLLATE NOCASE",[fieldDict["email"]] ) 
        email = cur.fetchone() 
        if not email == None:
            flash("Email address already registered!")
            return render_template("employeeregister.html",form=form,countries=countries)      
        
        # hash the password
        password=generate_password_hash(fieldDict["password"]) 

        # get the BooleanField value
        if "public_profile" in fieldDict:
            publicprofile = 1
        else:
            publicprofile = 0  
        
        # update the user table 
        cur.execute("INSERT INTO user values(null,3,?,?,?,?,?,?,?,?,?,?,?,?,?,0,null,CURRENT_TIMESTAMP)",[
         fieldDict["company"],fieldDict["firstname"],
         fieldDict["lastname"], fieldDict["phone"],  
         fieldDict["email"], fieldDict["address1"],  
         fieldDict["address2"], fieldDict["city"],  
         fieldDict["state"], fieldDict["zipcode"],  
         fieldDict["country"], password,
         publicprofile]
         )
        con.commit()
        cur.close     

        # update the session user_id
        cur.execute("SELECT id FROM user WHERE email = ?",[fieldDict["email"]] ) 
        user=cur.fetchone()
        session["user_id"] = user["id"]
        userid = user["id"]
        #update the geo_location table
        geo(userid)

        return render_template("index.html")        
       
    return render_template("employeeregister.html",form=form,countries=countries)      


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()
    # get the form
    form = loginform()   

    #check if the form is valid
    if request.method == "POST":   
        # Query database for username
        cur.execute("SELECT * FROM user WHERE email = ?", [request.form.get("email")])
        userrow=cur.fetchone()
       
        # Ensure email exists and password is correct
        if userrow == None:
            flash("Email does not exist! Please register this email address.")
            return render_template("login.html",form=form)
        elif  not check_password_hash(userrow["password"], request.form.get("password")):
            flash("Password is incorrect! Please renter your password.")
            return render_template("login.html",form=form)
        else:
            #Remember which user has logged in
            session["user_id"] = userrow["id"]
            #if user is a company rember the company
            if userrow["typeid"] == 1:
                session["company_id"] = userrow["companyid"]
                return redirect("/employee_managment")
            elif userrow["typeid"] == 3:
                return redirect("/cafes")          

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html",form=form)

@app.route("/logout")
def logout():  

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@login_required
@company_required
@app.route("/employee_managment", methods=["GET", "POST"])
def employee_managment():
    if request.method == "POST":          
        # check if the approved checkbox is checked
        if request.form.get("approvedcheck") == None:
            approved = 0            
        else:
            approved =  1    
        userid = request.form.get("userid")   
        
        # # update the approved status of the employees
        cur.execute("UPDATE user SET approved = ?, \
         approved_date = CASE when ? = 0 THEN NULL ELSE CURRENT_TIMESTAMP END WHERE id = ?", [approved,approved,userid]) 
        return redirect("/employee_managment")                   
 
    # get the employees for the company logged in 
    cur.execute("SELECT c.company, CASE WHEN u.approved = 0 THEN ""'No'"" ElSE ""'Yes'""   END approved  , \
    CASE WHEN u.approved_date IS NULL THEN ""' '""  ELSE date(u.approved_date,""'localtime'"" ) END approved_date, \
    u.firstname, u.lastname, date(u.timestamp,""'localtime'"" )timestamp, u.id \
    FROM user u JOIN company c ON u.companyid = c.id WHERE u.typeid=3 and companyid=? ORDER BY u.firstname, u.lastname",[session["company_id"]])    
    employrow = cur.fetchall() 

    # get the company information
    cur.execute("SELECT company FROM company WHERE id=?",[session["company_id"]])
    comprow = cur.fetchone()     

    return render_template("employee_managment.html",employrow=employrow,comprow=comprow)

@login_required
@app.route("/cafes", methods=["GET", "POST"])
def cafes():
    userid = session["user_id"]     
   
    # get the geo location of the user
    cur.execute("SELECT * FROM geo_location WHERE userid =?", [userid])
    location=cur.fetchone()   
    if location:
        locuser = (location["latitude"] , location["longitude"])
    else:
        locuser = None    

    # get a list of the vendors 
    cur.execute("SELECT c.id companyid, c.company, c.image, c.hour_start, c.hour_end,  c.website, u.address1, u.address2, u.city, u.state, u.phone, u.zipcode,  \
        address1 || ', ' || city || ', ' || zipcode address, g.latitude, g.longitude  \
        FROM company c LEFT JOIN user u on c.id = u.companyid LEFT JOIN geo_location g on u.id = g.userid WHERE c.typeid = 2")
    cafes = cur.fetchall()
    cafelist = []

    # get the longitude and latitude of the cafes 
    for cafe in cafes:         
        if cafe["latitude"] and  cafe["longitude"] and locuser !=None:
            loccafe = (cafe["latitude"] , cafe["longitude"])  
            #find the distence from the user
            dist = str(round(geodesic(locuser,loccafe).kilometers,2)).lstrip('0')     
            # create dict from row
        else:
            dist = '0'    
        dictcafe = dict_from_row(cafe)
        # append distence to the dict  
        dictcafe["distance"]  = dist 
        # append dict to list of rows
        cafelist.append(dictcafe)    

    # sort the dicts in the list of cafes   
    cafelist = sorted(cafelist, key = lambda i: i['distance'])

    return render_template("cafes.html",cafes=cafelist)  

@login_required
@app.route("/cafe_signup", methods=["GET", "POST"])
def cafe_signup():     
    form= CafeSignupForm()  
      
    # check the session cafe 
    if request.args.get('companyid') != None:
        session["cafe_id"] = request.args.get('companyid')
    
    if session.get("cafe_id") == None:       
        return redirect("/login")      
    else:    
        companyid = session["cafe_id"]     
    
    # select the company information
    cur.execute("SELECT c.id companyid, c.company, c.image, c.hour_start, c.hour_end,  c.website, u.address1, u.address2, u.city, u.state, u.phone, u.zipcode,  \
        address1 || ', ' || city || ', ' || zipcode address  \
        FROM company c LEFT JOIN user u on c.id = u.companyid where c.typeid = 2 and c.id=?", [companyid])
    cafe = cur.fetchone()  

    # select all the employees in the cafe with date greater or equal then today
    cur.execute("SELECT c.*, u.firstname , u.lastname FROM cafe_signup c JOIN user u ON c.userid =u.id \
        WHERE u.public = 1 and c.companyid=? and c.date >= DATE() ORDER BY c.date, c.start_time, u.firstname, u.lastname",[companyid])   
    people = cur.fetchall() 

    # create a time select list with the start and end time of the cafe hours
    (start_hour, start_min)=cafe["hour_start"].split(":")
    (end_hour, end_min)=cafe["hour_end"].split(":")
    def datetime_range(start, end, delta):
        current = start
        while current <= end:        
            yield current        
            current += delta    
    cafetimes_start = [(str(dt).split(" ",1)[1])[:-3] for dt in 
       datetime_range(datetime.datetime(1900, 1, 1,int(start_hour),int(start_min)), datetime.datetime(1900, 1, 1, int(end_hour)-1, int(end_min)), 
       timedelta(minutes=15))        
       ]
    cafetimes_end = [(str(dt).split(" ",1)[1])[:-3] for dt in 
       datetime_range(datetime.datetime(1900, 1, 1,int(start_hour)+1,int(start_min)), datetime.datetime(1900, 1, 1, int(end_hour), int(end_min)), 
       timedelta(minutes=15))        
       ]   
    form.start_time.choices = cafetimes_start
    form.end_time.choices = cafetimes_end       

    if form.validate_on_submit():
        # get the data from the forms
        fieldDict={}        
        for key in request.form.keys():
            fieldDict[key]= request.form.get(key)           
        
        # get the signup time in minutes            
        (h, m) = fieldDict["start_time"].split(':')
        resultstart = int(h) * 60 + int(m)
        (h, m) = fieldDict["end_time"].split(':')
        resultend = int(h) * 60 + int(m) 
        minutes = resultend - resultstart    
        
        # update the cafe_signup table 
        if fieldDict["companyid"] != "":            
            cur.execute("INSERT INTO cafe_signup values(null,?,?,?,?,?,?,0)",
            [session["user_id"],fieldDict["companyid"],
            fieldDict["date"], fieldDict["start_time"],  
            fieldDict["end_time"], minutes])
        else:
            flash("You must select a cafe!")             
        con.commit()
        cur.close 
        return redirect("/cafe_signup")                     

    # check if the user was approved
    userid = session["user_id"]
    cur.execute("SELECT approved FROM user where id = ? and approved = 1", [userid])
    user = cur.fetchone()  

    if user:
        return render_template("cafe_signup.html", form=form, cafe=cafe, people=people)       
    else:
        flash("Employer has not yet approved transactions!")
        return redirect("/cafes")
   
        

@login_required
@app.route("/cafe_reservations", methods=["GET", "POST"])
def cafe_reservations():
    # update the canceled reservation
    if request.method == "POST":
        id = request.form.get("id")                   
        cur.execute("UPDATE cafe_signup SET canceled = 1 WHERE id = ?",[id])    
        con.commit()
        cur.close

    # get a list of future reservations
    userid = session["user_id"]
    cur.execute("SELECT s.*, c.company AS cafe FROM cafe_signup s JOIN user u ON s.userid = u.id JOIN company c ON s.companyid =c.id \
        WHERE s.userid = ? AND (s.date > Date() OR (s.start_time > time() and s.date=Date())) and canceled = 0 ORDER BY s.date, s.start_time",[userid])
    reservations = cur.fetchall()  

    return render_template("cafe_reservations.html", reservations=reservations)  

@login_required
@app.route("/account_update", methods=["GET", "POST"])
def account_update(): 
    userid = session["user_id"]

    #get the account information
    cur.execute("SELECT u.*, c.company FROM user u JOIN company c ON u.companyid = c.id  WHERE u.id = ?", [userid])
    account = cur.fetchone()   
    form = AccountUpdateForm(country=account["countryid"])         

    # get a list of countries from the database 
    cur.execute("SELECT id,name FROM countries")
    countries = cur.fetchall()         
    form.country.choices = [( " ","Select" )] + [(country["id"],country["name"]) for country in countries]    
  
    if form.validate_on_submit():           
        # get the data from the forms
        fieldDict={}        
        for key in request.form.keys():
            fieldDict[key]= request.form.get(key)  
        
        #set the boolean field
        if account["typeid"] == 3:
            if "public_profile" in fieldDict:
                publicprofile = 1
            else:
                publicprofile = 0  
        else:
            publicprofile = account["public"]           

        #update the account
        cur.execute("UPDATE user SET firstname = ?, lastname = ?, phone = ?, address1 = ?, address2 = ?, city = ?, state = ?, zipcode = ?, countryid = ?, public = ? \
        WHERE id = ?", \
        [fieldDict["firstname"], fieldDict["lastname"], fieldDict["phone"], fieldDict["address1"], fieldDict["address2"], \
        fieldDict["city"], fieldDict["state"],  fieldDict["zipcode"], fieldDict["country"], publicprofile, userid])
        con.commit()
        cur.close
       
        #update the geo_location table
        geo(userid)

        # update the company table
        if  session.get("company_id") != None:
            if fieldDict["company"] != "" :  
                companyid = session["company_id"]    
                cur.execute("UPDATE company SET company = ? WHERE id = ?",[fieldDict["company"], companyid]) 
                con.commit()
                cur.close  
                             
        return redirect ("/")  
    else: 
        return render_template("account_update.html", form=form, account=account, countries=countries)  
    
    
@login_required
@app.route("/password_update", methods=["GET", "POST"])
def password_update(): 
    form = PasswordUpdateForm()
    userid = session["user_id"]
    
    if form.validate_on_submit():    
        password = request.form.get("password")
        # hash the password
        password = generate_password_hash(password) 
        # update the user table
        cur.execute("UPDATE user set password = ? where id = ?",[password,userid])
        con.commit()
        cur.close

        return redirect ("/")    
    else: 
        return render_template("password_update.html", form=form)      


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
