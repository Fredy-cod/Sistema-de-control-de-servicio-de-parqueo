from flask import Flask, render_template, session, redirect, request, url_for
from lib.database import database

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
    join_str=db.join("propietarios", "vehiculos")
    if request.method=="POST" and not "username" in session:
        username= request.form.get("username")
        password= request.form.get("password")
        users= db.getRecords("nombre_usuario, contrasenha", "playas")
        return render_template("main.html", customers= db.getRecords("placa, nombre_completo", join_str)) #Eliminar para verificación
        for i in users:
            if i[1] == password and i[0] == username:
                session["username"]= username
                return render_template("main.html", customers= db.getRecords("placa, nombre_completo", join_str))   
    elif "username" in session:
        return render_template("main.html", customers= db.getRecords("placa, tipo, nombre_completo", join_str)) 
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "username" in session:
        session.clear()
    return redirect(url_for("init"))


if __name__=="__main__":
    app.run(debug=True)
