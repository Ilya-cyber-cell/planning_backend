# -*- encoding: utf-8 -*-

from mysql.connector import connect, Error
from .HttpError import HttpError
from .dbStructure import dbStructure

class dbConnection:
    dict_tables=dbStructure.dict_tables
    def __init__(self, app):
        self.app = app  
        self.connection=self.connect_to_db();
        
    def __del__(self):
        self.connection.close
        print("Разорвано подключение к БД")

    def connect_to_db(self):
        print("Подключаюсь к БД")
        try:
            connection = connect(
                host=self.app.config['DB_HOST'],
                user=self.app.config['DB_USER'],
                password=self.app.config['DB_PASSWORD'],
                db=self.app.config['DB_NAME']
            )
            return connection
        except Error as e:
            print(e)
            raise HttpError('505',str(e))

    def get_connected_table(self,table):
        res=[]
        for field in self.dict_tables[table]:
            print(field)
            if self.dict_tables[table][field]['type']=='link_to':
                res.append({'field':field,'link':self.dict_tables[table][field]['link_table']})
        return res
