from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/pythonmongodb'

mongo = PyMongo(app)

@app.route("/users", methods=['POST'])
def create_user():
    name = request.json['name']
    mail = request.json['mail']
    password = request.json['password']

    if name and mail and password:
        hashed_password = generate_password_hash(password)

        id = mongo.db.users.insert({
            'name': name,
            'mail': mail,
            'password': hashed_password
        })

        response = {
            'id': str(id),
            'name': name,
            'mail': mail,
            'password': hashed_password
        }

        return response
    else:
        return not_found()
    return {'message': 'received'}

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)

    return Response(response, mimetype="application/json")

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)

    return Response(response, mimetype="application/json")

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route('/users/<id>', methods=['PUT'])
def edit_user(id):
    name = request.json['name']
    mail = request.json['mail']
    password = request.json['password']

    if name and mail and password:
        hashed_password = generate_password_hash(password)

        id = mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'name': name,
            'mail': mail,
            'password': hashed_password
        }})

        response = {
            'id': str(id),
            'name': name,
            'mail': mail,
            'password': hashed_password
        }

        return response
    
    else:
       return not_found() 
    

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'REesorce Not Found: ' + request.url,
        'status': 404
    })

    response.state_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True, port=3000)

