from flask import Flask, render_template, session, redirect, request
from flask_session import Session
from lib.database import database
from datetime import datetime

#variables generales del servidor de BBDD
servidor="db4free.net" 
puerto=3306
usuario="sanpablo22"
contrasenha="sanpablo22"
nombre_bd="parking_system"

db= database(servidor, puerto, usuario, contrasenha, nombre_bd)
#db.close()


app= Flask(__name__)

@app.route("/")
def init():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    #Hacer verificacion de usuario
    user= [request.form.get("username"), request.form.get("password"), request.form.get("user_type")]
    
    return render_template("main.html", customers= db.getRecords("id_cliente, nombres", "clientes"))

if __name__=="__main__":
    app.run(debug=True)
