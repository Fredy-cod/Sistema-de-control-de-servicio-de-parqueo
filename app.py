from flask import Flask, render_template, session
from flask_session import Session


app= Flask(__name__)

@app.route("/")
def init():
    return render_template("home.html", message="Hola soy Fredy")



if __name__=="__main__":
    app.run(debug=True)
