from flask import Flask, render_template, session, redirect, request, url_for
from flask_session import Session
from lib.database import database
from datetime import datetime

#variables generales del servidor de BBDD
kwargs= {
    "host":"127.0.0.1",
    "port":3306,
    "user":"root",
    "password":"sanpablo22",
    "db_name":"parkingSystem"
    }

db= database(**kwargs)
#db.close()


app= Flask(__name__)

app.secret_key="sanpablo22"

@app.route("/")
def init():
    return render_template("home.html")

@app.route("/login")
def login():
    if "username" in session:
        session.clear()
    return render_template("login.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    if request.method=="POST" and not "username" in session:
        session["username"]= request.form.get("user")
        cadena=db.join("propietarios", "vehiculos")
        return render_template("main.html", customers= db.getRecords("placa, nombre_completo", cadena))        
    else:
        return redirect(url_for("init"))

@app.route("/logout")
def logout():
    #Eliminar el elemento user
    return redirect(url_for("init"))

if __name__=="__main__":
    app.run(debug=True)
