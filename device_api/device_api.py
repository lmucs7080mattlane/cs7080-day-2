import datetime
from flask import Flask, request, abort, jsonify, render_template_string
from pymongo import MongoClient
from bson.objectid import ObjectId
app = Flask(__name__)


# http://docs.mongodb.com/getting-started/python/client/
mongo_database = None
mongo_credentials_collection = None
mongo_session_collection = None
mongo_sensor_data_collection = None
def connect_to_mongo():
    global mongo_database
    global mongo_credentials_collection
    global mongo_session_collection
    global mongo_sensor_data_collection
    client = MongoClient('mongodb://mongo:27017/devices')
    # Cheap and easy command to test the connection
    client.admin.command('ismaster')
    mongo_database = client.get_default_database()
    mongo_credentials_collection = mongo_database.credentials
    mongo_session_collection = mongo_database.session
    mongo_sensor_data_collection = mongo_database.sensor_data
connect_to_mongo()


def return_error(code):
    return ('', code)

def return_empty_success():
    return return_error(200)

@app.route('/login/', methods = ['POST'])
def handle_login():
    login_credentials = request.get_json()
    if 'device_name' not in login_credentials or 'password' not in login_credentials:
        return return_error(400)


    # TODO Challenge. The mongo_credentials_collection stores JSON documents
    # with two properties: 'device_name' and 'password'. See if you can find
    # a match to the login_credentials we received
    matching_credentials = mongo_credentials_collection.find_one(
        {
            'device_name': login_credentials['device_name'],
            'password': login_credentials['password']
        }
    )

    # TODO If you cannot find a match, return a 401 Unauthorised error
    if matching_credentials is None:
        return return_error(401)

    # TODO Otherwise, insert a new JSON document in the mongo_session_collection
    # with a single property 'device_name'.
    # Return the 'inserted_id' of the inserted document, the connected
    # device will use this id as it's session id.
    result = mongo_session_collection.insert_one(
        {
            'device_name': login_credentials['device_name']
        }
    )
    return jsonify(str(result.inserted_id))

@app.route('/sensor_data/', methods = ['POST'])
def handle_sensor_data():
    request_body = request.get_json()
    if 'session_id' not in request_body \
       or 'device_name' not in request_body \
       or 'sensor_data' not in request_body:
        return return_error(400)

    # TODO Challenge: First verify that the session_id and device_name
    # properties of the request body match a document in mongo_session_collection
    matching_session = mongo_session_collection.find_one(
        {
            'device_name': request_body['device_name'],
            '_id': ObjectId(request_body['session_id'])
        }
    )

    # TODO If you cannot find a matching session, return a 401 Unauthorised error.
    if matching_session is None:
        return return_error(401)

    # TODO Otherwise, insert a new document into the mongo_sensor_data_collection
    # with the properties 'device_name', 'sensor_data' and 'timestamp'
    # You can get the current timestamp by calling datetime.datetime.now()
    result = mongo_sensor_data_collection.insert_one(
        {
            'device_name': request_body['device_name'],
            'sensor_data': request_body['sensor_data'],
            'timestamp': datetime.datetime.now()
        }
    )

    # TODO return the new document's inserted_id
    return jsonify(str(result.inserted_id))

if __name__ == '__main__':
    app.run()