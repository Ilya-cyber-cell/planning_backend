# -*- encoding: utf-8 -*-

from .dbConnection import dbConnection
from .HttpError import HttpError
from mysql.connector import  Error


class dictionaryEditor(dbConnection):
    table_name=""
    fields = []
    fields_type={}
    def select_dictionary(self,table_name):
        alowed_tables = ['servers','data_center','client','project','application']
        if table_name not in alowed_tables:
            raise HttpError('404','NotAlowed')
        self.table_name=table_name
        self.fields=[]
        self.fields_type={}
        for field in  self.dict_tables[table_name]:
            self.fields.append(field) 
            self.fields_type[field]=self.dict_tables[table_name][field]['type']
        
    # подгтовка списка полей        
    def preparation_list_field(self):
        table=self.table_name
        result=""
        fild_name=[]
        human_readable_field_name=[]
        for field in self.dict_tables[table]:
                if self.dict_tables[table][field]["type"] == "link_to":
                    parent_table=self.dict_tables[table][field]["link_table"]
                    link_field=self.dict_tables[table][field]["link_field"]
                    for parent_field in self.dict_tables[parent_table]:
                        if parent_field != link_field:
                            result=result+ parent_table + "." + parent_field + ", "
                            fild_name.append(parent_table + "." + parent_field)
                            human_readable_field_name.append(self.dict_tables[parent_table][parent_field]["human_name"])
                else:
                    result=result + table+"."+field + ", "
                    fild_name.append(table+"."+field)
                    human_readable_field_name.append(self.dict_tables[table][field]["human_name"])
        return result[:-2] , fild_name,human_readable_field_name
    
    # Поготовка строки со списком таблиц из которых надо выбрать данные
    def preparation_from(self):
        table=self.table_name
        result="From " + table 
        for field in self.dict_tables[table]:
            if self.dict_tables[table][field]["type"] == "link_to":
                parent_table=self.dict_tables[table][field]["link_table"]
                link_field=self.dict_tables[table][field]["link_field"]
                join_type = " LEFT JOIN "
                if  "notnull" in self.dict_tables[table][field]:
                    if self.dict_tables[table][field]["notnull"]:
                        join_type = " JOIN "
                result = result + join_type + parent_table + " ON " + table + "." + field + " = " + parent_table +"." + link_field + " "
                        

        return result   
    
    def get_data(self,id=None):
        if id==None:
           return self.get_all_row()
        else:
           return self.get_single_row(id)
                
    def get_all_row(self,id=None):
        result={} 
        list_field,columns,human_readable_field_name = self.preparation_list_field()
        select_from = self.preparation_from()
        if id==None:
            show_table_query = "SELECT " + list_field + " " + select_from
        else:
            show_table_query = "SELECT " + list_field + " " + select_from + " WHERE " + self.fields[0] + " = " + str(id)
        results=[]
        print(show_table_query)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(show_table_query)
                for row in cursor.fetchall():
#                    results.append(dict(zip(columns, row)))
                    results.append(row)

                cursor.fetchall()
            if len(results) > 0 :
                if id==None:
                    result = {"error":0,"data":results,"field_name":columns,"human_readable_field_name":human_readable_field_name}
                else:
                    result = {"error":0,"data":results[0],"field_name":columns,"human_readable_field_name":human_readable_field_name}
            else:
                raise HttpError('404','Not found')
        except Error as e:
            result = {"error":1,"data":str(e)}
        except Exception as ex:
            result = {'error':ex.expression,'data':ex.message}
        return result


    def get_single_row(self,id):
        table=self.table_name
        parent_tables=self.get_parent_table(table)
        result={} 
        (field_name, list_field)= self.get_field_name(table)
        show_table_query = "SELECT " + list_field  + " FROM " + table + " WHERE " + self.fields[0] + " = " + str(id)
        results=[]
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(show_table_query)
                for row in cursor.fetchall():
                    i=0
                    for field in row:
                        results.append({"value":field,**field_name[i]})  
                        i=i+1
            if len(results) > 0 :
                result = {"error":0,"data":results,'parent_tables':parent_tables}
            else:
                raise HttpError('404','Not found')
        except Error as e:
            result = {"error":1,"data":str(e)}
        except Exception as ex:
            result = {'error':ex.expression,'data':ex.message}
        return result
    
    def get_table_structure(self):
        table=self.table_name
        parent_tables=self.get_parent_table(table)
        (field_name, list_field)= self.get_field_name(table)
        return {"error":0,"data":field_name,'parent_tables':parent_tables}
    
    def get_field_name(self,table):
        field_name=[]
        list_field=""
        for field in self.dict_tables[table]:
            if "link_table" in self.dict_tables[table][field]:
                field_name.append({"name":field,"human_readable_field_name":self.dict_tables[table][field]["human_name"],"link_table":self.dict_tables[table][field]["link_table"]})
            elif "hidden" in self.dict_tables[table][field]:
                field_name.append({"name":field,"human_readable_field_name":self.dict_tables[table][field]["human_name"],"hidden":1})
            else:
                field_name.append({"name":field,"human_readable_field_name":self.dict_tables[table][field]["human_name"]})
            list_field= list_field + field + ", "        
        return field_name, list_field[:-2]
    
    def get_parent_table(self,table):
#        res=[]
        res={}
        for field in self.get_connected_table(table):
            parent_table=self.get_parent_table_content(field['link'])
#            res.append({field['field']:parent_table})
            res[field['link']]=parent_table
        return res
        
    def get_parent_table_content(self,table):
        show_table_query = "SELECT * FROM " + table
        results={}
        with self.connection.cursor() as cursor:
            cursor.execute(show_table_query)
            for row in cursor.fetchall():
                results[row[0]]=row[1]
            cursor.fetchall()
        return results        

    def save_data(self,entry_id,post_data):
        table=self.table_name
        list_value=[]
        where=""
        set_list=""
        for fild in post_data['SaveData']:
            if self.fields_type[fild['name']] == 'auto_increment':
                where=" WHERE " + fild['name'] + " = " + str(fild['value']) 
            else:
                set_list = set_list +  fild['name'] + " = %s ,"
                list_value.append(fild['value'])
        show_query ="UPDATE " + table + "  SET "+ set_list[:-1] + where
        print(show_query)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(show_query,list_value)
                result = {"error":0,"data":''}
                self.connection.commit()
        except Error as e:
            result = {"error":1,"data":str(e)}
        except Exception as ex:
            result = {'error':ex.expression,'data':ex.message}
        return result
    
    def add_data(self,post_data):
        table=self.table_name
        list_field=[]
        list_value=[]
        for fild in post_data['SaveData']:
            if "value" in fild:
                print (fild['name'] + str(fild['value']))
                list_field.append(fild['name'])
                list_value.append(fild['value'])
        sql="INSERT INTO " + table + " (" + ''.join(", ".join(list_field)) + ") VALUES (" + ''.join(", ".join(["%s" for x in range(len(list_field))]))  + ")"
        print(sql)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql,list_value)
                result = {"error":0,"data":''}
                self.connection.commit()
        except Error as e:        
            result = {"error":1,"data":str(e)}
        except Exception as ex:
            result = {'error':ex.expression,'data':ex.message}
        return result














