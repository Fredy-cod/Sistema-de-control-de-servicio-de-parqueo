#from crypt import methods
from flask import Flask, render_template, session, redirect, request, url_for
#from importlib_metadata import method_cache
from lib.database import database

#variables generales del servidor de BBDD
kwargs= {
    "host":"127.0.0.1",
    "port":3306,
    "user":"root",
    "password":"sanpablo2022",
    "db_name":"parkingSystem"
    }

db= database(**kwargs)
#db.close()

admin_key="sanpablo22"

app= Flask(__name__)

app.secret_key="sanpablo22"

#Variables globales
join_car_abo=db.join("abonados", "vehiculos")

@app.route("/")
def init():
    return render_template("home.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if "username" in session:
        return redirect(url_for("main"))
    if request.method=='POST': #Verificación del usuario
        username= request.form.get("username")
        password= request.form.get("password")
        users= db.getRecords("nombre_usuario, contrasenha, id_playa", "playas")
        #return render_template("main.html", customers= db.getRecords("placa, tipo, nombre_completo", join_str), 
        #                        employees= db.getConditionalRecords("doc_id, nombre_completo, telefono, concat('S/.',salario)", "empleados", "id_playa=4000")) #Eliminar para verificación
        for i in users:
            if i[1] == password and i[0] == username:
                session["username"]= i[0]
                session["user_id"]= int(i[2])
                main_kwargs={
                    "customers": db.getRecords("placa, tipo, nombre_completo", join_car_abo),
                    "employees": db.getConditionalRecords("doc_id, nombre_completo, telefono, concat('S/.',salario)", "empleados", f"id_playa={session['user_id']}"),
                    "subscribers_ids": db.getRecords("id_abonado", "abonados")
                }
                return render_template("main.html", admin_validated=0, **main_kwargs)
    return render_template("login.html")



@app.route("/main", methods=["GET", "POST"])
def main():
    if not "username" in session:
        return redirect(url_for("login"))
    main_kwargs={
            "customers": db.getRecords("placa, tipo, nombre_completo", join_car_abo),
            "employees": db.getConditionalRecords("doc_id, nombre_completo, telefono, concat('S/.',salario)", "empleados", f"id_playa={session['user_id']}"),
            "subscribers_ids": db.getRecords("id_abonado", "abonados")
        }
    if request.method == "POST" and "username" in session:
        form_name= request.form.get("form_name")
        if form_name == "ticket_generate":
            db.addRecord("tickets", request.form.get("car_id"), f"(null, {session['user_id']}, curdate(), curtime())")
        elif form_name == "":
            pass
        elif form_name == "":
            pass
        elif form_name == "append_employee":
            pass
        elif form_name == "admin_valid":
            if request.form.get('admin_password') == admin_key:
                return render_template("main.html", admin_validated=1, **main_kwargs)
            else:
                return render_template("main.html", admin_validated=0, **main_kwargs)

    elif request.method != "POST" and "username" in session:
        return render_template("main.html", admin_validated=0, **main_kwargs)

@app.route("/logout")
def logout():
    if "username" in session:
        session.clear()
    return redirect(url_for("init"))


if __name__=="__main__":
    app.run(debug=True)
