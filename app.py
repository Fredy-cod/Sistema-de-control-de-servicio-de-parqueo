from flask import Flask, render_template, session
from flask_session import Session
from pymysql import *
import pymysql

#variables generales del servidor de BBDD
servidor="db4free.net" 
puerto=3306
usuario="sanpablo22"
contrasenha="sanpablo22"
nombre_bd="parking_system"

database= pymysql.connect(host=servidor, port=puerto, user=usuario, passwd=contrasenha, db=nombre_bd)

cursor= database.cursor()
cursor.execute("select * from Regiones;")
consulta= cursor.fetchall()
print(consulta)
database.close()

'''
app= Flask(__name__)

@app.route("/")
def init():
    return render_template("home.html", message="Hola soy Fredy")



if __name__=="__main__":
    app.run(debug=True)
'''