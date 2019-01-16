from flask import Flask, render_template, redirect
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
    #return render_template("data_analysis.html")
    return redirect("http://10.7.145.192:8053")

@app.route("/best")
def best():
    #return render_template("best.html")
    return redirect("http://10.7.145.192:8051")

@app.route("/worst")
def worst():
    #return render_template("worst.html")
    return redirect("http://10.7.145.192:8052")
