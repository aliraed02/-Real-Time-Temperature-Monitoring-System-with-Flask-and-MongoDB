from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
import random
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/sensors'  # Replace with your MongoDB URI



uri = "mongodb+srv://aliraed3003:aliraed3003@cluster0.16t8j4r.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


socketio = SocketIO(app)
mongo = PyMongo(app)


@socketio.on('connect')
def handle_connect():
    print('Client connected')



@app.route('/temperature')
def get_temperature():
    temperature = mongo.db.temperature.find_one()  # Retrieve temperature from MongoDB
    if temperature:
        socketio.emit('temperature_update', temperature['value'])  # Emit temperature to connected clients
        return 'Temperature emitted to clients'
    else:
        return 'No temperature data found'






# Insert sample temperature data

@app.route('/new', methods=['POST'])
def set_temperature():
    
    #temperature = request.form.get('temperature')

    
    temperature_data = {
        'value': random.randint(1, 101),  # Replace with your temperature value
        'timestamp': datetime.now()

    }   
   
   # Process the temperature data and save it
   
   
    mongo.db.temperature.insert_one(temperature_data)
    
    return " "



if __name__ == '__main__':
    app.run()
    #socketio.run(app)
    
    
    
    

