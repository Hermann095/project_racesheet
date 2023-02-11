import os
from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from simulation.sim import startTestQualifying, disconnectionHandler
import json as JSON
import numbers


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

mode = "dev"

if ("MODE" in os.environ):
    mode = os.environ["MODE"]


react_folder = "../react-frontend"
directory= os.getcwd()+ f'/{react_folder}/build/static'


@app.route('/')
@app.route('/results')
@app.route('/standings')
def index():
    if (mode == "prod"):
        path= os.getcwd()+ f'/{react_folder}/build'
        print(path)
        return send_from_directory(directory=path,path='index.html')
    else:
        return send_from_directory(os.getcwd(), path="index.html")



@app.route('/static/<folder>/<file>')
def css(folder,file):
    if (mode == "prod"):
        path = folder+'/'+file
        return send_from_directory(directory=directory,path=path)
    else:
        return


@app.route("/drivers", methods=["GET"])
def get_drivers():
    return {"drivers": [{"name": "Gerhard Berger", "nationality": "AUT"}, {"name": "Niki Lauda", "nationality": "AUT"}, {"name": "Mauricio Gugelmin", "nationality": "BRA"}]}

@app.route("/qualifying")
def run_qualifying():
    result = startTestQualifying(False, socketio)
    return result

@app.route("/carset")
def get_carset_path():
    #dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../carsets/test123/"))
    #carset_path = Path(dir_path)
    #carset_path = file_path.parents[0] / "/carsets/test123/"
    return {"name": "test123"}


@socketio.on("connect")
def connected():
    print(request.sid)
    print("client connected")
    emit("connect",{"data":f"id: {request.sid} is connected"})

@socketio.on("disconnect")
def disconnected():
    disconnectionHandler()
    print("client disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)

@socketio.on("run_qualifying")
def run_ws_qualifying(json):
    print("recieved run_qualifying")
    print((str(json)))
    #printResults = JSON.loads(json)
    simSpeed = 1

    if "simSpeed" in json:
            newSimSpeed = json["simSpeed"]
            if isinstance(newSimSpeed, numbers.Number):
                simSpeed = newSimSpeed

    result = startTestQualifying(json["printResults"], socketio, simSpeed)
    #emit("update_qualifying_results", result)




if __name__ == '__main__':
    socketio.run(app, debug=True)