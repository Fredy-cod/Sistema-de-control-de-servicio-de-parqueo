#from crypt import methods
from flask import Flask, render_template, session, redirect, request, url_for
#from importlib_metadata import method_cache
from lib.database import database
from datetime import datetime
import json

#variables generales del servidor de BBDD
kwargs= {
    "host":"127.0.0.1",
    "port":3306,
    "user":"root",
    "password":"sanpablo2022",
    "db_name":"parking"
    }

db= database(**kwargs)
#db.close()

admin_key="sanpablo22"

app= Flask(__name__)

app.secret_key="sanpablo22"

#Variables globales
admin_validated=0
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
        for i in users:
            if i[1] == password and i[0] == username:
                session["username"]= i[0]
                session["user_id"]= int(i[2])
                main_kwargs={
                    "subscribers": db.getRecords("abonados.id_abonado, nombre_completo, fecha_inicio, fecha_final, placa, tipo", join_car_abo),
                    "employees": db.getConditionalRecords("doc_id, nombre_completo, telefono, concat('S/.',salario)", "empleados", f"id_playa={session['user_id']}"),
                    "subscribers_ids": db.getRecords("id_abonado", "abonados"),
                    "boletas": db.getRecords("id_boleta, id_vehiculo, hora_ingreso, hora_salida, precio", db.join("tickets", "boletas")),
                    "NoBoletas": db.getRecords("tickets.id_ticket, placa, hora_ingreso ",f"vehiculos inner join tickets on tickets.id_vehiculo = vehiculos.placa and tickets.id_playa = {session['user_id']} inner join boletas on tickets.id_ticket != boletas.id_ticket order by tickets.id_ticket desc")
                    }
                return render_template("main.html", admin_validated=admin_validated, **main_kwargs)
    return render_template("login.html")


@app.route("/main", methods=["GET", "POST"])
def main():
    global admin_validated
    if not "username" in session:
        return redirect(url_for("login"))
    main_kwargs={
            "subscribers": db.getRecords("abonados.id_abonado, nombre_completo, fecha_inicio, fecha_final, placa, tipo", join_car_abo),
            "employees": db.getConditionalRecords("doc_id, nombre_completo, telefono, concat('S/.',salario)", "empleados", f"id_playa={session['user_id']}"),
            "subscribers_ids": db.getRecords("id_abonado", "abonados"),
            "boletas": db.getRecords("id_boleta, id_vehiculo, hora_ingreso, hora_salida, precio", db.join("tickets", "boletas")),
            "NoBoletas": db.getRecords("tickets.id_ticket, placa, hora_ingreso ",f"vehiculos inner join tickets on tickets.id_vehiculo = vehiculos.placa and tickets.id_playa = {session['user_id']} inner join boletas on tickets.id_ticket != boletas.id_ticket order by tickets.id_ticket desc")
            }
    if request.method == "POST" and "username" in session:
        form_name= request.form.get("form_name")
        if form_name == "ticket_generate":
            car_ids= db.getRecords("placa", "vehiculos")
            car_dates= [request.form.get("car_id"), request.form.get("car_type"), request.form.get('subscriber_id')]
            if car_dates[2]!="":
                db.addRecordIgnore("vehiculos", f"('{car_dates[0]}', {int(car_dates[2])}, '{car_dates[1]}')")
            else:
                db.addRecordIgnore("vehiculos", f"('{car_dates[0]}', null, '{car_dates[1]}')")
            db.addRecord("tickets", f"(null, '{ car_dates[0] }', '{session['user_id']}', curdate(), curtime())")
            main_kwargs={
                "subscribers": db.getRecords("abonados.id_abonado, nombre_completo, fecha_inicio, fecha_final, placa, tipo", join_car_abo),
                "employees": db.getConditionalRecords("doc_id, nombre_completo, telefono, concat('S/.',salario)", "empleados", f"id_playa={session['user_id']}"),
                "subscribers_ids": db.getRecords("id_abonado", "abonados"),
                "boletas": db.getRecords("id_boleta, id_vehiculo, hora_ingreso, hora_salida, precio", db.join("tickets", "boletas")),
                "NoBoletas": db.getRecords("tickets.id_ticket, placa, hora_ingreso ",f"vehiculos inner join tickets on tickets.id_vehiculo = vehiculos.placa and tickets.id_playa = {session['user_id']} inner join boletas on tickets.id_ticket != boletas.id_ticket order by tickets.id_ticket desc")
                }
            return render_template("main.html", admin_validated=admin_validated, **main_kwargs)
        elif form_name == "gen_boleta":
            id_ticket= request.form.get("ticket_id")
            datas= db.getConditionalRecords("tarifa, hora_inicio", db.join("playas", "tickets"), f"id_ticket={ id_ticket }")
            actual= str(datetime.now().time())
            minutes= int(db.query_executor(f"TIMESTAMPDIFF(minute, time({ datas[1] }), time({ actual }))"))
            minutes= minutes/60
            db.addRecord("boletas", f"(null, { id_ticket }, { float(int(datas[0])*minutes) }, curtime())")
            main_kwargs={
                "subscribers": db.getRecords("abonados.id_abonado, nombre_completo, fecha_inicio, fecha_final, placa, tipo", join_car_abo),
                "employees": db.getConditionalRecords("doc_id, nombre_completo, telefono, concat('S/.',salario)", "empleados", f"id_playa={session['user_id']}"),
                "subscribers_ids": db.getRecords("id_abonado", "abonados"),
                "boletas": db.getRecords("id_boleta, id_vehiculo, hora_ingreso, hora_salida, precio", db.join("tickets", "boletas")),
                "NoBoletas": db.getRecords("tickets.id_ticket, placa, hora_ingreso ",f"vehiculos inner join tickets on tickets.id_vehiculo = vehiculos.placa and tickets.id_playa = {session['user_id']} inner join boletas on tickets.id_ticket != boletas.id_ticket order by tickets.id_ticket desc")
                }
            return render_template("main.html", admin_validated=admin_validated, **main_kwargs)
        elif form_name=="add_subscriber":
            subscriber_data=[request.form.get("subs_fullname"), request.form.get("subs_init"), request.form.get("subs_end"), float(request.form.get("subs_pension"))]
            db.addRecord("abonados", f"(null, '{subscriber_data[0]}', date({subscriber_data[1]}), date({subscriber_data[2]}), '{subscriber_data[3]}')")
            main_kwargs={
                "subscribers": db.getRecords("abonados.id_abonado, nombre_completo, fecha_inicio, fecha_final, placa, tipo", join_car_abo),
                "employees": db.getConditionalRecords("doc_id, nombre_completo, telefono, concat('S/.',salario)", "empleados", f"id_playa={session['user_id']}"),
                "subscribers_ids": db.getRecords("id_abonado", "abonados"),
                "boletas": db.getRecords("id_boleta, id_vehiculo, hora_ingreso, hora_salida, precio", db.join("tickets", "boletas")),
                "NoBoletas": db.getRecords("tickets.id_ticket, placa, hora_ingreso ",f"vehiculos inner join tickets on tickets.id_vehiculo = vehiculos.placa and tickets.id_playa = {session['user_id']} inner join boletas on tickets.id_ticket != boletas.id_ticket order by tickets.id_ticket desc")
                }
            return render_template("main.html", admin_validated=admin_validated, **main_kwargs)
        elif form_name == "delete_employee":
            employee_id= int(request.form.get('employee_id'))
            db.deleteRecords("empleados", f"id_empleado= {employee_id}")
            main_kwargs={
                "subscribers": db.getRecords("abonados.id_abonado, nombre_completo, fecha_inicio, fecha_final, placa, tipo", join_car_abo),
                "employees": db.getConditionalRecords("doc_id, nombre_completo, telefono, concat('S/.',salario)", "empleados", f"id_playa={session['user_id']}"),
                "subscribers_ids": db.getRecords("id_abonado", "abonados"),
                "boletas": db.getRecords("id_boleta, id_vehiculo, hora_ingreso, hora_salida, precio", db.join("tickets", "boletas")),
                "NoBoletas": db.getRecords("tickets.id_ticket, placa, hora_ingreso ",f"vehiculos inner join tickets on tickets.id_vehiculo = vehiculos.placa and tickets.id_playa = {session['user_id']} inner join boletas on tickets.id_ticket != boletas.id_ticket order by tickets.id_ticket desc")
                }
            return render_template("main.html", admin_validated=1, **main_kwargs)
        elif form_name == "append_employee": #Agregar registro a Empleados
            employee_data= [int(request.form.get('doc_id')), request.form.get('fullname'), int(request.form.get('phone')), float(request.form.get('salary'))]
            db.addRecordIgnore("empleados", f"({employee_data[0]}, {session['user_id']},'{employee_data[1]}', {employee_data[2]}, {employee_data[3]})")
            main_kwargs={
                "subscribers": db.getRecords("abonados.id_abonado, nombre_completo, fecha_inicio, fecha_final, placa, tipo", join_car_abo),
                "employees": db.getConditionalRecords("doc_id, nombre_completo, telefono, concat('S/.',salario)", "empleados", f"id_playa={session['user_id']}"),
                "subscribers_ids": db.getRecords("id_abonado", "abonados"),
                "boletas": db.getRecords("id_boleta, id_vehiculo, hora_ingreso, hora_salida, precio", db.join("tickets", "boletas")),
                "NoBoletas": db.getRecords("tickets.id_ticket, placa, hora_ingreso ",f"vehiculos inner join tickets on tickets.id_vehiculo = vehiculos.placa and tickets.id_playa = {session['user_id']} inner join boletas on tickets.id_ticket != boletas.id_ticket order by tickets.id_ticket desc")
                }
            return render_template("main.html", admin_validated=admin_validated, **main_kwargs)
        elif form_name == "admin_valid": #Validar contraseña del administrador
            if request.form.get('admin_password') == admin_key:
                admin_validated=1
                return render_template("main.html", admin_validated=admin_validated, **main_kwargs)
            else:
                return render_template("main.html", admin_validated=admin_validated, **main_kwargs)
        elif form_name == "delete_employee": #Eliminar un empleado de la BBDD
            employee_id= int(request.form.get('employee_id'))
            db.deleteRecords('empleados', f'id_empleado={int(employee_id)}')
            main_kwargs={
                "subscribers": db.getRecords("abonados.id_abonado, nombre_completo, fecha_inicio, fecha_final, placa, tipo", join_car_abo),
                "employees": db.getConditionalRecords("doc_id, nombre_completo, telefono, concat('S/.',salario)", "empleados", f"id_playa={session['user_id']}"),
                "subscribers_ids": db.getRecords("id_abonado", "abonados"),
                "boletas": db.getRecords("id_boleta, id_vehiculo, hora_ingreso, hora_salida, precio", db.join("tickets", "boletas")),
                "NoBoletas": db.getRecords("tickets.id_ticket, placa, hora_ingreso ",f"vehiculos inner join tickets on tickets.id_vehiculo = vehiculos.placa and tickets.id_playa = {session['user_id']} inner join boletas on tickets.id_ticket != boletas.id_ticket order by tickets.id_ticket desc")
            }
            return render_template("main.html", admin_validated=admin_validated, **main_kwargs)
        elif form_name == "modify_employee": #Modificar datos de un empleado de la BBDD
            employee_id= int(request.form.get('employee_id'))
            employee_data= db.getConditionalRecord('telefono, salario, nombre_completo', 'empleados', f"id_empleado= '{ employee_id }'")
            empl_phone= int(request.form.get('new_phone')) if request.form.get('new_phone')!="" else employee_data[0] 
            empl_salary= float(request.form.get('new_salary')) if request.form.get('new_salary')!="" else employee_data[1]
            db.modRecords("empleados", f"salario={ empl_salary }, telefono={ empl_phone }", f"nombre_completo='{ employee_data[2] }'")
            main_kwargs={
                "subscribers": db.getRecords("abonados.id_abonado, nombre_completo, fecha_inicio, fecha_final, placa, tipo", join_car_abo),
                "employees": db.getConditionalRecords("doc_id, nombre_completo, telefono, concat('S/.',salario)", "empleados", f"id_playa={session['user_id']}"),
                "subscribers_ids": db.getRecords("id_abonado", "abonados"),
                "boletas": db.getRecords("id_boleta, id_vehiculo, hora_ingreso, hora_salida, precio", db.join("tickets", "boletas")),
                "NoBoletas": db.getRecords("tickets.id_ticket, placa, hora_ingreso ",f"vehiculos inner join tickets on tickets.id_vehiculo = vehiculos.placa and tickets.id_playa = {session['user_id']} inner join boletas on tickets.id_ticket != boletas.id_ticket order by tickets.id_ticket desc")
            }
            return render_template("main.html", admin_validated=admin_validated, **main_kwargs)
    elif request.method != "POST" and "username" in session:
        return render_template("main.html", admin_validated=admin_validated, **main_kwargs)

@app.route("/logout")
def logout():
    global admin_validated
    if "username" in session:
        session.clear()
        admin_validated= 0
    return redirect(url_for("init"))


if __name__=="__main__":
    app.run(debug=True)
