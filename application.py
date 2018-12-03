import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps

app = Flask(__name__)

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
            return render_template('error.html', message= f"The user {user} is logged in")
        
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
            return render_template("registered.html")
        else:
            return render_template("error.html", message=f"The user {user} already exists" )
        return render_template("error.html", message="no fue posible guardar los datos en el servidor" )


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
        u = db.execute("SELECT * FROM users WHERE username = :user", {"user": request.form['user']}).fetchone()
        stored_password = u[4]
        if check_password_hash(stored_password, request.form['password']):
            session['username'] = u[1]
            return render_template('loggedin.html')
        else:
            return render_template('error.html', message="your password is not correct")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("loggedout"))

@app.route("/loggedout")
def loggedout():
    return render_template("loggedout.html")

@app.route("/loggedin")
def loggedin():
    return render_template("loggedin.html")

######

@app.route("/search", methods=["POST", "GET"])
@login_required
def search():
    if request.method == "GET":
        return render_template("search.html", results=None)
    if request.method == "POST":
        #print(request.form['search'])
        try:
            year = int(request.form['search'])
            results = db.execute("SELECT * FROM books WHERE (year = :year)", { "year": year})
        except ValueError:
            results = db.execute("SELECT * FROM books WHERE (title LIKE :search OR author LIKE :search OR isbn LIKE :search )",
                    { "search": "%"+str(request.form['search']).lower()+"%" }).fetchall()
        print(results) #OR title LIKE :search OR author LIKE :search
        return render_template("search.html",results=results)

