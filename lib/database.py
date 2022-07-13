import this
import pymysql
import json

class database:
    def __init__(self, host, port, user, password, db_name):
        self.db= pymysql.connect(host=host, port=port, user=user, passwd=password, db=db_name)
        self.cursor= self.db.cursor()
    def addRecord(self, table, values):
        '''Añade un registro con los valores 'value' a la tabla 'table'.'''
        try:
            self.cursor.execute(f"""INSERT INTO {table} 
                                    VALUES {values};""")
            self.db.commit()
        except ValueError:
            print(f'Error en la inserción a la tabla {table}')
        finally:
            pass
            #self.cursor.close()
    def addRecordIgnore(self, table, values):
        '''Añade un registro con los valores 'value' a la tabla 'table'.'''
        try:
            self.cursor.execute(f"""INSERT IGNORE {table} 
                                    VALUES {values};""")
            self.db.commit()
        except ValueError:
            print(f'Error en la inserción a la tabla {table}')
        finally:
            pass
    def query_executor(self, function):
        try:
            self.cursor.execute(f"SELECT {function};")
            return self.cursor.fetchone()
        except ValueError:
            pass
        finally:
            pass
    def modRecords(self, table, values, condition):
        '''Modifica un registro existente en 'table'.'''
        try:
            self.cursor.execute(f"""UPDATE {table} 
                                    SET { values }
                                    WHERE { condition };""")
            self.db.commit()
        except ValueError:
            print(f'Error en la modificación a la tabla {table}')
        finally:
            pass
    def getRecords(self, columns, table):
        '''Obtiene la respuesta de una consulta SELECT de SQL.'''
        try:
            self.cursor.execute(f"""SELECT {columns}
                                    FROM {table};""")
            return self.cursor.fetchall()
        except ValueError:
            print("Error en la consulta")
        finally:
            pass
            #self.cursor.close()
    def getConditionalRecords(self, columns, table, conditions):
        '''Obtiene la respuesta de una consulta SELECT condicionada de SQL.'''
        try:
            self.cursor.execute(f"""SELECT {columns} 
                                    FROM {table} 
                                    WHERE {conditions};""")
            return self.cursor.fetchall()
        except ValueError:
            print("Error en la consulta")
        finally:
            pass
            #self.cursor.close()
    def getConditionalRecord(self, columns, table, conditions):
        '''Obtiene un registro de una consulta SELECT condicionada de SQL.'''
        try:
            self.cursor.execute(f"""SELECT {columns} 
                                    FROM {table} 
                                    WHERE {conditions};""")
            return self.cursor.fetchone()
        except ValueError:
            print("Error en la consulta")
        finally:
            pass
    def deleteRecords(self, table, condition):
        '''Elimina los registros de la tabla TABLE con una CONDITION.'''
        try:
            self.cursor.execute(f"""DELETE FROM {table}
                                    WHERE {condition}""")
        except ValueError:
            print("Error en la eliminación")
        finally:
            pass
    def join(self, *args):
        '''Retorna un string con el QUERY indicado para realizar una consulta SQL.
            Ejemplo:
            join("casas", "veredas", "postes"...):
            Retorna: "casas INNER JOIN veredas ON casas.id_casa = veredas.id_casa INNER JOIN postes ON veredas.id_vereda = postes.id_vereda".'''
        query= f"{args[0]} "
        for index in range(1, len(args)):
            query += f"INNER JOIN {args[index]} ON {args[index-1]}.id_{args[index-1][:-1]} = {args[index]}.id_{args[index-1][:-1]} "
        return query
    def filter(self, table, **kwargs):
        query = f"SELECT * FROM {table}"
        i = 0
        for key, value in kwargs.items():
            if i == 0:
                query += " WHERE "
            else:
                query += " AND "
            query += "{}='{}'".format(key, value)
            i += 1
        query += ";"
        return query
    def close(self):
        '''Cierra la conexión con el servidor.'''
        self.db.close()
    """
    def addRecords(self, table, listValues):
        '''Añade más de un registro con los valores 'value' a la tabla 'table'.'''
        try:
            for i in listValues:
                self.cursor.execute(f""""""INSERT INTO {table} 
                                        VALUES {tuple(listValues[i])};"""""")
            self.db.commit()
        except ValueError:
            print(f'Error en la inserción a la tabla {table}')
        finally:
            pass
            #self.cursor.close()"""

    def actualization(self, main_kwargs, join_car_abo, user_id):
        main_kwargs= {
            "subscribers": self.getRecords("abonados.id_abonado, nombre_completo, fecha_inicio, fecha_final, placa, tipo", join_car_abo),
            "employees": self.getConditionalRecords("doc_id, nombre_completo, telefono, concat('S/.',salario)", "empleados", f"id_playa={user_id}"),
            "subscribers_ids": self.getRecords("id_abonado", "abonados"),
            "boletas": self.getRecords("id_boleta, id_vehiculo, hora_ingreso, hora_salida, precio", self.join("tickets", "boletas")),
            "NoBoletas": self.getRecords("tickets.id_ticket, placa, hora_ingreso ",f"vehiculos inner join tickets on tickets.id_vehiculo = vehiculos.placa and tickets.id_playa =  {user_id} inner join boletas on tickets.id_ticket != boletas.id_ticket order by tickets.id_ticket desc;")
        }