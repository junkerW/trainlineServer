# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import trainline_finder as train
from json2html import *
from datetime import datetime
import json


app = Flask(__name__)


def encode(string:str):
    return string.encode('utf8')


@app.route('/')
def hello():
    return '<h1>Bahn Backend</h1>'


@app.route('/bahn/list')
def bahn_raw():
 return render_template('bahn.html')


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

    final = train.find_cheapest_connections(start_station, destinations, start_date_towards, end_date_towards,
                                            start_date_back, end_date_back, max_duration, bus=bus, train=trains)

    if ret_type == 'json':
        return json.dumps(final)
    else:
        return json2html.convert(json=final)


app.run(host='0.0.0.0')
