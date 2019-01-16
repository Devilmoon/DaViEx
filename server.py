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
    return render_template("co2_emissions.html")

@app.route("/data_analysis")
def app1():
    return render_template("data_analysis.html")


@app.route("/best")
def best():
    return render_template("best.html")

@app.route("/worst")
def worst():
    return render_template("worst.html")
