import pymysql
import numpy as np

class database:
    def __init__(self, host, port, user, password, db_name):
        self.db= pymysql.connect(host=host, port=port, user=user, passwd=password, db=db_name)
        self.cursor= self.db.cursor()
    def addRecord(self, table, values):
        '''Añade un registro con los valores 'value' a la tabla 'table'.'''
        try:
            self.cursor.execute(f"""INSERT INTO %s 
                                    VALUES %s;""", table, values)
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
                                        VALUES {listValues[i]};""")
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
    def close(self):
        '''Cierra la conexión con el servidor.'''
        self.db.close()