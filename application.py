from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    headLine = "head"
    return render_template("index.html", headLine=headLine)

@app.route("/carlos")
def carlos():
    return "Hello, Carlos"

@app.route("/<string:name>")
def hello(name):
    return f"Hello, {name}"

@app.route("/more")
def more():
    return render_template("more.html")