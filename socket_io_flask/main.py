import eventlet
eventlet.monkey_patch()
import eventlet.wsgi
import socketio
from flask import Flask, render_template, request
import os
import urlparse
import requests
import json

app = Flask(__name__)
app.config.from_envvar('CONFIG_PATH')
for i in app.config:
    os.environ[i] = str(app.config[i])

mgr = socketio.KombuManager(app.config["REDIS_URL"])
sio = socketio.Server(client_manager=mgr,ping_timeout=30,ping_interval=15)


# /update_sio_token/
def update_sid(auth_token,sid):
    url = "%s/update_sid/" % os.environ["API_URL"]
    headers = {"X-Auth-Token":auth_token}
    payload = {"sid":sid}
    r = requests.post(url,headers=headers,json=payload) 
    print "Updated: ",sid, auth_token
    if r.status_code==200:
        return True
    return False
 
# /delete_sio_token/
def delete_sid(sid):
    url = "%s/delete_sid/" % os.environ["API_URL"]
    payload = {"sid":sid}
    r = requests.post(url,json=payload) 
    return

@app.route('/')
def index():
    return ""

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    auth_token = environ.get("HTTP_AUTH_TOKEN","")
    qs = environ.get("QUERY_STRING")
    args = urlparse.parse_qs(qs)
    if args.has_key("auth_token"):
        auth_token = args["auth_token"][0]
    if not auth_token:
        return False    
    return update_sid(auth_token,sid)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)
    # Send SID
    delete_sid(sid) 

port = app.config["SOCKET_IO_PORT"]

if __name__ == '__main__':
    app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', port)), app)
