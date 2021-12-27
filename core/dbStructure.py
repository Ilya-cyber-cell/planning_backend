# -*- encoding: utf-8 -*-


class dbStructure:
        dict_tables={"servers":{
                         "servers_id":{"type":"auto_increment","human_name":"Идентификатор записи","hidden":1},
                         "name": {"type":"text","indx":"unique","notnull":True,"human_name":"Название"},                        
                         "name_zabbix":{"type":"text","human_name":"Название zabbix"},
                         "name_client":{"type":"text","human_name":"Название клиента"},
                         "data_center_id":{"type":"link_to","link_table":"data_center","link_field":"data_center_id","notnull":True,"human_name":"Дата центр"},
                         "deleted":{"type":"bit","human_name":"Запись удалена"}
                    },
                    "data_center":{
                        "data_center_id":{"type":"auto_increment","human_name":"Идентификатор записи"},
                        "name":{"type":"TEXT","human_name":"Название датацентра"},
                        "deleted":{"type":"bit","human_name":"Запись удалена"}
                    },
                    "instanse":{
                        "instanse_id":{"type":"auto_increment","human_name":"Идентификатор записи"},
                        "server_id":{"type":"link_to","link_table":"servers","link_field":"servers_id","human_name":"Сервер"},
                        "application_id":{"type":"link_to","link_table":"application","link_field":"application_id","human_name":"Приложение"},
                        "name_clickhouse":{"type":"TEXT","human_name":"Название в clickhouse"},
                        "deleted":{"type":"bit","human_name":"Запись удалена"}
                    }, 
                    "client":{
                        "client_id":{"type":"auto_increment","human_name":"Идентификатор записи"},
                        "name":{"type":"TEXT","human_name":"Название"},
                        "deleted":{"type":"bit","human_name":"Запись удалена"}
                    },
                    "project":{
                        "project_id":{"type":"auto_increment","human_name":"Идентификатор записи"},
                        "name":{"type":"TEXT","human_name":"Название"},
                        "deleted":{"type":"bit","human_name":"Запись удалена"}
                    },
                    "application":{
                        "application_id":{"type":"auto_increment","human_name":"Идентификатор записи"},
                        "client_id":{"type":"link_to","link_table":"client","link_field":"client_id","human_name":"Клиент"},
                        "name":{"type":"TEXT","human_name":"Название"},
                        "url":{"type":"TEXT","human_name":"URL"},
                        "project_id":{"type":"link_to","link_table":"project","link_field":"project_id","human_name":"Проект"},
                        "deleted":{"type":"bit","human_name":"Запись удалена"}
                       },
                    }
                        
