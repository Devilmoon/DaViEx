from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/world")
def world():
    return render_template("world.html")