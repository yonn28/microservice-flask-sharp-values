from flask import Flask, jsonify
import pandas as pd
from itertools import cycle
from flask_cors import CORS
from flask_sslify import SSLify
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)





@app.route('/api/v1/x', methods=['GET'])
def ploting_get_x():
    return jsonify([1,2,3,4])




if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0',port=8080) #change port to 8080 for deployment, and host = '0.0.0.0'