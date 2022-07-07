import pymysql
import numpy as np

class database:
    def __init__(self, host, port, user, password, db_name):
        self.db= pymysql.connect(host=host, port=port, user=user, passwd=password, db=db_name)
        self.cursor= self.db.cursor()
    def addRecord(self, table, values):
        '''Añade un registro con los valores 'value' a la tabla 'table'.'''
        try:
            self.cursor.execute(f"""INSERT INTO {table} 
                                    VALUES {tuple(values)}""")
            self.db.commit()
        except ValueError:
            print(f'Error en la inserción a la tabla {table}')
        finally:
            pass
            #self.cursor.close()
    def addRecords(self, table, listValues):
        '''Añade más de un registro con los valores 'value' a la tabla 'table'.'''
        try:
            for i in listValues:
                self.cursor.execute(f"""INSERT INTO {table} 
                                        VALUES {tuple(listValues[i])};""")
                self.db.commit()
        except ValueError:
            print(f'Error en la inserción a la tabla {table}')
        finally:
            pass
            #self.cursor.close()
    def getRecords(self, columns, table):
        '''Obtiene la respuesta de una consulta SELECT de SQL.'''
        try:
            self.cursor.execute(f"""SELECT {columns}
                                    FROM {table};""")
            return np.array(self.cursor.fetchall())
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
            return np.array(self.cursor.fetchall())
        except ValueError:
            print("Error en la consulta")
        finally:
            pass
            #self.cursor.close()
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