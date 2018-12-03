import os, requests

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps

app = Flask(__name__)

KEY = "CaDB8T0wy4uZdikS5yqRw"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

SECRET_KEY="klajsdmfklsdjiovjzxckvn213987}{ñ+´.-sd"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        if 'username' in session:
            return redirect(url_for('index'))
        else:
            return render_template("register.html")
        
    if request.method == "POST":
        context = request.form
        user = context['user']
        #check if there is a user already logged in
        if 'username' in session:
            user = session['username']
            return render_template('error.html', message= { "message": f"The user {user} is logged in", "type": "info" })
        
        #check if the user is already in the database
        if db.execute("SELECT * FROM users WHERE username = :user",{"user": user}).rowcount == 0:
            #log in the user
            session['username'] = user
            #if not, create the user
            name,email,user = context['name'],context['email'],context['user']
            hashed_value=generate_password_hash(context['password'], method='sha256')
            db.execute("INSERT INTO users ( name, email, username, password) VALUES (:name, :email, :username, :password )",
                    { "name": name, "email": email, "username": user, "password": hashed_value } )
            db.commit()
            return render_template("registered.html",  message={ "message": "You have been registered successfully", "type": "success" })
        return render_template("error.html", message={ "message": "no fue posible guardar los datos en el servidor", "type": "warning" } )


#from flask import g, request, redirect, url_for
##The decorator for restricting views to loggedin users
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))

    return decorated_function

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if 'username' in session:
            return redirect(url_for('index'))
        else:
            return render_template("login.html")
    if request.method == "POST":
        userdata = db.execute("SELECT * FROM users WHERE username = :user", {"user": request.form['user']}).fetchone()
        if userdata == None:
            return render_template('error.html', message={ "message": "your username or password is not correct", "type": "warning" } )
        elif check_password_hash(userdata[4], request.form['password']):
            session['username'] = userdata[1]
            return render_template('loggedin.html', message={ "message": "You have succesfully logged in!", "type": "success" })
        else:
            return render_template('error.html', message={ "message": "your username or password is not correct", "type": "warning" })


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("loggedout"))

@app.route("/loggedout")
def loggedout():
    return render_template("loggedout.html", message={ "message": "You have logged out", "type": "info" })

@app.route("/loggedin")
def loggedin():
    return render_template("loggedin.html",  message={ "message": "You have successfully logged in", "type": "success" })

######

@app.route("/search", methods=["POST", "GET"])
@login_required
def search():
    if request.method == "GET":
        return render_template("search.html", results=None)
    if request.method == "POST":
        #print(request.form['search'])
        #try for the case of typing the year
        try:
            year = int(request.form['search'])
            results = db.execute("SELECT * FROM books WHERE (year = :year) ORDER BY title", { "year": year}).fetchall()
        except ValueError:
            results = db.execute("SELECT * FROM books WHERE (title LIKE :search OR author LIKE :search OR isbn LIKE :search )",
                    { "search": "%" + str(request.form['search']).lower() + "%" }).fetchall()
        #print(results) #OR title LIKE :search OR author LIKE :search
        return render_template("search.html",results=results,  message={ "message": "The searching proccess was succesful!", "type": "info" })

@app.route("/book/<string:isbn>", methods=["POST", "GET"])
@login_required
def book(isbn):
    #Get bookdata from the database, bookdata_GR from google reads, and the review info
    bookdata = db.execute("SELECT * FROM books WHERE (isbn = :isbn)", { "isbn": isbn}).fetchone()
    bookdata_GR = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbn })
    review = db.execute("SELECT * FROM reviews WHERE username = :username AND isbn = :isbn", { "username": session['username'], "isbn": isbn }).fetchone()
    if bookdata == None:
        return render_template("error.html", message={ "message": "The book you are looking for it does not exists", "type": "warning" })
    if request.method == "GET" :
        return render_template("book.html", bookdata_GR=bookdata_GR.json()["books"][0], bookdata=bookdata, review=review)
    elif request.method == "POST":
        print(request.form)
        if review == None:
            db.execute("INSERT INTO reviews ( isbn, username, review, rate) VALUES (:isbn, :username, :review, :rate )",
                        { "isbn": isbn, "username": session['username'], "review": request.form['review'], "rate": request.form['rate'] } )
            db.commit()
            message={ "message": "Your review has been submited", "type": "success" }
        else:
            db.execute("UPDATE reviews SET review = :review, rate = :rate WHERE username = :username AND isbn = :isbn",
                        { "isbn": isbn, "username": session['username'], "review": request.form['review'], "rate": request.form['rate'] } )
            db.commit()
            message={ "message": "Your review has been updated", "type": "info" }
        return render_template("book.html", bookdata_GR=bookdata_GR.json()["books"][0], 
            bookdata=bookdata, review={ "review": request.form['review'], "rate": int(request.form['rate']) },
            message=message)

