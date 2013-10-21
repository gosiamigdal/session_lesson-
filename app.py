from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    return render_template("login.html")

@app.route("/youshouldprobablychangethisurl")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug = True)
