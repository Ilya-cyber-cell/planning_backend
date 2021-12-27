#!../bin/python3
#-*-coding:utf-8-*-
from flask import Flask,jsonify,abort,make_response,request
from flask_cors import CORS
import core 

app = Flask(__name__,static_url_path='')
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': str(error)}), 404)

@app.route('/api/dict/<string:table>',methods=['GET'])
def get_dict(table):
    try:
        dict_editor = core.dictionaryEditor(app)
        dict_editor.select_dictionary(table)
        return jsonify(dict_editor.get_all_row()) 
    except Exception as ex:
        return jsonify({'error':ex.expression,'data':ex.message})
    
@app.route('/api/dict/<string:table>',methods=['POST'])
def add_new_entry(table):
    try:
        dict_editor = core.dictionaryEditor(app)
        dict_editor.select_dictionary(table)
        if 'data' in request_data:
            return jsonify(dict_editor.add_data(request_data['data']))  
    except Exception as ex:
        return jsonify({'error':ex.expression,'data':ex.message})

@app.route('/api/dict/<string:table>/',methods=['GET'])
@app.route('/api/dict/<string:table>/<int:entry_id>',methods=['GET'])
def get_dict_entry(table,entry_id=None):
    try:
        dict_editor = core.dictionaryEditor(app)
        dict_editor.select_dictionary(table)
        if entry_id == None:
            return jsonify(dict_editor.get_table_structure()) 
        else:
            return jsonify(dict_editor.get_single_row(entry_id)) 
    except Exception as ex:
        print(ex)
        return jsonify({'error':ex.expression,'data':ex.message})
    
@app.route('/api/dict/<string:table>/',methods=['POST'])
@app.route('/api/dict/<string:table>/<int:entry_id>',methods=['POST'])
def save_dict_entry(table,entry_id=None):
    request_data = request.get_json()
    try:
        dict_editor = core.dictionaryEditor(app)
        dict_editor.select_dictionary(table)
        if 'data' in request_data:
            if entry_id == None:
                return jsonify(dict_editor.add_data(request_data['data']))
            else:
                return jsonify(dict_editor.save_data(entry_id,request_data['data'])) 
    except Exception as ex:
        print(ex)
        return jsonify({'error':ex.expression,'data':ex.message})


    
@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': str(error)}), 404)


if __name__ == '__main__':
    dbInit = core.dbInit(app)
    dbInit.Init()
    del dbInit
    app.run(host=app.config['FLASK_RUN_HOST'], port=app.config['FLASK_RUN_PORT'])

 























