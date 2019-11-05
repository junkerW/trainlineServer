# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from bahn import trainline_finder as train
from json2html import *
from datetime import datetime
import json
import socket
import logging

app = Flask(__name__)

hostName = socket.gethostname()
hostIP = socket.gethostbyname(hostName)
port = 5000

logger = app.logger
logger.setLevel('INFO')
fh = logging.FileHandler('/var/log/bahn/log.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

train = train.TrainlineFinder(logger)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255',1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def encode(string:str):
    return string.encode('utf8')


@app.route('/')
def hello():
    return '<h1>Bahn Backend</h1>'


@app.route('/bahn/list')
def bahn_raw():
 return render_template('bahn.html', host=get_ip(), port=port)


@app.route('/bahn/radius/')
def bahn_radius():
    return render_template('bahn_radius.html')


@app.route('/bahn/api/list/<ret_type>', methods=['GET'])
def bahn_post(ret_type):
    data = request.args

    destinations = data.get('destinations').split(',')
 #   for i in range(len(destinations)):
 #       destinations[i] = encode(destinations[i])

    start_station = data.get('start_station')
    start_date_towards = datetime.strptime(data.get('start_date_towards'), '%Y-%m-%dT%H:%M')
    end_date_towards = datetime.strptime(data.get('end_date_towards'), '%Y-%m-%dT%H:%M')
    start_date_back = datetime.strptime(data.get('start_date_back'), '%Y-%m-%dT%H:%M')
    end_date_back = datetime.strptime(data.get('end_date_back'), '%Y-%m-%dT%H:%M')

    max_duration = int(data.get('max_duration')) * 60

    transport = data.get('transport')
    trains = True
    bus = True
    if transport == 'train':
        bus = False
    if transport == 'bus':
        trains = False

    try:
        final = train.find_cheapest_roundtrips(start_station, destinations, start_date_towards, end_date_towards,
                                               start_date_back, end_date_back, max_duration, bus=bus, train=trains)
    except Exception as e:
        logger.error("Error finding Connection: {}".format(e))
        return "Error finding Connections", 500


    if ret_type == 'json':
        return json.dumps(final)
    else:
        return json2html.convert(json=final)


logger.info("Starting Bahn Flask app on {}:{}".format(get_ip(), port))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

