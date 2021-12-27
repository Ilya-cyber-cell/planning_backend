# -*- encoding: utf-8 -*-

from .dbConnection import dbConnection
from .HttpError import HttpError
from mysql.connector import  Error


class dbInit(dbConnection):
    def Init(self):
        print("init")
        exist_table = self.get_all_exist_table()
        for table in self.dict_tables:
            if table not in exist_table:
                self.create_new_table(table,self.dict_tables[table])
            exist_field=self.get_table_field(table) 
            last_field=""
            # добавление новых проей
            for field in self.dict_tables[table]:
                if field not in exist_field:
                    self.add_field(table, field,self.dict_tables[table][field],last_field)
                last_field=field
        #На момент созжания индесов все таблицы должны существовать
        for table in self.dict_tables:
            # создание индексов
            exist_IDX=self.get_index(table)
            for field in self.dict_tables[table]:
                if "indx" in self.dict_tables[table][field] :
                    if field not in exist_IDX:
                        self.add_index(table,field,"index_type")
            # создание внешних ключей
            exist_FK=self.get_FK(table)
            for field in self.dict_tables[table]:
                if self.dict_tables[table][field]["type"] == "link_to" and (field not in exist_FK):   
                    self.add_FK(table,field,self.dict_tables[table][field]["link_table"],self.dict_tables[table][field]["link_field"])

    
    def type_field(self,field_struct):
        sql=""
        null_alowed = "NULL"
        if "notnull" in field_struct:
            if field_struct["notnull"]:
                null_alowed = "NOT NULL"
        if field_struct["type"] == "auto_increment":
            sql =  " INT NOT NULL AUTO_INCREMENT"
        elif field_struct["type"] == "link_to":
            sql =  " INT  "+ null_alowed
        else:        
            sql =  field_struct["type"] +"  "+ null_alowed 
        return sql
            
    def get_all_exist_table(self):
        results=[]
        all_tables = "show tables"
        with self.connection.cursor() as cursor:
            cursor.execute(all_tables)
            for row in cursor.fetchall():
                results.append(row[0])
        return results 
    
    def create_new_table(self,table_name,table_struct):
        print("create_new_table: " + table_name)
        create_table="CREATE TABLE `" + table_name + "` ("
        key_field=""
        for field in table_struct:
            sql = self.type_field(table_struct[field])
            if table_struct[field]["type"] == "auto_increment":
                key_field = field
            create_table = create_table +" " +field + " " + sql  + ", " 
        if key_field != "":
            create_table = create_table + " PRIMARY KEY ("+ key_field +")) "    
            print (create_table)
            with self.connection.cursor() as cursor:
                cursor.execute(create_table)
        else:
            print ("Не определен PRIMARY KEY для таблицы:" +  table_name) 

    def get_table_field(self,table_name):
        show_table_query = "DESCRIBE " + table_name
        results=[]
        with self.connection.cursor() as cursor:
            cursor.execute(show_table_query)
            for row in cursor.fetchall():
                results.append(row[0])
        return results
            
            
    def add_field(self,table_name,field,field_struct,after=""):
        print("add_field:" + table_name + " field:" + str(field))
        sql = self.type_field(field_struct)
        if after=="":
            alter_table = "ALTER TABLE "+table_name+" ADD "+field+" "+ sql
        else:
            alter_table = "ALTER TABLE "+table_name+" ADD "+field+" "+ sql +" AFTER "+ after
        print (alter_table)
        with self.connection.cursor() as cursor:
             cursor.execute(alter_table)  

    def get_index(self,table):
        show_table_query = "SHOW INDEX FROM "+table+" FROM "+ self.app.config['DB_NAME']+" ;"
        results=[]
        with self.connection.cursor() as cursor:
            cursor.execute(show_table_query)
            for row in cursor.fetchall():
                results.append(row[4])        
        return results
    
    def add_index(self,table_name,field,index_type):
        print("add_index:" + table_name + " field:" + str(field))
        alter_table = "ALTER TABLE "+table_name + " ADD UNIQUE ("+field+"); "
        print (alter_table)
        with self.connection.cursor() as cursor:
             cursor.execute(alter_table)   
             
    def get_FK(self,table):
        show_table_query = """SELECT TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME, REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME
                            FROM  INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                            WHERE REFERENCED_TABLE_SCHEMA = '"""+ self.app.config['DB_NAME'] +"' AND TABLE_NAME = '"+table+"';"
        results=[]
        with self.connection.cursor() as cursor:
            cursor.execute(show_table_query)
            for row in cursor.fetchall():
                results.append(row[1])        
        return results
        
        
    def add_FK(self,table_name,field,link_table,link_field):
        print("add_FK:" + table_name + " field:" + str(field))
        alter_table = "ALTER TABLE "+table_name + " ADD FOREIGN KEY ("+field+") REFERENCES "+link_table+"("+link_field+") ON DELETE RESTRICT ON UPDATE RESTRICT;     "
        print (alter_table)
        with self.connection.cursor() as cursor:
             cursor.execute(alter_table)         
        
        
        
        
        
        
        
        
        
        

