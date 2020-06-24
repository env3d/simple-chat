import gevent
import gevent.monkey
gevent.monkey.patch_all()

from flask import Flask
from flask import send_from_directory, send_file
from flask import Response, request, jsonify
from flask_sockets import Sockets
import json
from collections import deque
from datetime import datetime
import os
import re
import threading

import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
sockets = Sockets(app)

# Global data structures
messages = deque(maxlen=100)
message_available = gevent.event.Event()
open_sockets = []


@sockets.route('/ws')
def web_socket(ws):
    open_sockets.append(ws)
    while not ws.closed:
        msg = ws.receive()        
        print(f'message received: {msg}')
        append_message(msg)
    open_sockets.remove(ws)

@app.route('/stream')
def stream():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            message_available.wait()            
            yield f'data: {json.dumps(messages[0])}\n\n'
    return Response(eventStream(), mimetype="text/event-stream")

    
@app.route('/<string:filename>', defaults={"path":""})
@app.route('/<string:path>/<string:filename>')
def frontend(path, filename):
    print(f'serving {path}/{filename}')

    search_paths = ['./static/']
    file_path = [f'{search_path}/{path}/{filename}' for search_path in search_paths
                 if os.path.exists(f'{search_path}/{path}/{filename}')]

    response = send_file(file_path[0]) if len(file_path) > 0 else Response(status=404)

    return response

@app.route('/example1.html')
@app.route('/example2.html')
def server_generate_html():
    title = 'Example 1' if 'example1' in request.url_rule.rule else 'Example 2'
    messagesHTML = '\n'.join([ f'       <tr><td>{m["time"]}</td><td>{m["message"]}</td></tr>' for m in list(messages) ])
    refresh = '  <meta http-equiv="refresh" content="1">' if 'example2' in request.url_rule.rule else ''
    html = '\n'.join([
        '<html>',
        '<head>',
        '  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/kognise/water.css@latest/dist/light.min.css">',
        refresh,
        '</head>',
        '<body>',
        f'  <h1>{title}</h1>',        
        '  <form action="add_message" method="post">',
        '    <label>Post a message:</label><input type=text name="message" autocomplete="off">',
        '    <input type="submit">',  
        '  </form>',
        '  <table>',
        messagesHTML,
        '  </table>',
        '<body>',
        '</html>'
    ])
    return html

@app.route('/info')
def info():
    return jsonify({'message': 'basic chat app example'})

# Add a message
@app.route('/add_message', methods = ['GET','POST'])
def add_message():    
    message = request.args.get('message') or request.form.get('message')
    append_message(message)
    print(f'requestion from {request.referrer}')
    if re.search('(example1|example2)', request.referrer):
        print('adding header')
        res = Response(status=301)
        res.headers['Location'] = request.referrer
    else:
        res = jsonify(message)
    return res

# get all messages
@app.route('/messages')
def get_messages():
    return jsonify(list(messages))
    
    
def get_timestamp():
    # datetime object containing current date and time
    now = datetime.now()
    
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


def append_message(message):
    message_object = {'message':message, 'time':get_timestamp()}
    message_available.set()
    messages.appendleft(message_object)
    for ws in open_sockets:
        try:
            ws.send(json.dumps(message_object))
        except:
            pass
    message_available.clear()


import threading
import csv
import random

sample_messages = []
with open('sample_messages.csv') as csvfile:
    sample_reader = csv.reader(csvfile)    
    for row in sample_reader:
        sample_messages.append(row[5])
    
def populate_message():
    while True:
        random_message = sample_messages[ random.randrange(len(sample_messages)) ]
        #print(f'adding message {random_message}')
        append_message(random_message)
        delay = random.randrange(9)+1
        #print(f'  next message coming in {delay} seconds')
        gevent.sleep(delay)    
    
#populate_message()

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)

    srv_greenlet = gevent.spawn(server.start)
    background_task = gevent.spawn(populate_message)
    try:
        gevent.joinall([srv_greenlet, background_task])
    except KeyboardInterrupt:
        print("Exiting")
    
    #server.serve_forever()
