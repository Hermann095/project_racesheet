import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from simulation.sim import runTestQualifying


app = Flask(__name__)
CORS(app)

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
    result = runTestQualifying()
    return result


if __name__ == '__main__':
    app.run(debug=True, threaded=True)