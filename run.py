import io
import os
import RPi.GPIO as GPIO
import time
import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Response
import picamera

from  flask_restful import Resource, Api
from camerafun import capture_picture, gen_videos
# create our little application :)
app = Flask(__name__)

jsfile = "/home/pi/Documents/python/homecamera/camstate.json"

def read_state():
        with open(jsfile, 'r') as f:
                return json.load(f)

def write_state(state):
        with open(jsfile, 'w') as f:
                json.dump(state,f)
                
class CamInfo(Resource):

        def __init__ (self):
                filename = "/home/pi/Documents/python/homecamera/features.json"
                with open(filename,'r') as f:
                        self.info = json.load(f)
                print(self.info)

        def __str__(self):
                return self.info
        def get(self):
                return self.info


@app.route("/",methods=["GET","POST"])
def home():
   print("home")
   try:
       return render_template("/camera.html")
   except Exception as ex:
       print(ex)

@app.route("/change_mode",methods=["GET","POST"])
def change_mode():
   mode = request.form["mode"]
   return render_template("/camera.html",mode=mode)
  
@app.route('/take_picture')
def take_picture():
   caminfo = CamInfo()
   print("taking a picture")
   print(caminfo.info["name"])
   return Response(capture_picture(caminfo.info["name"],1),
   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/timelapse')
def timelapse():
   #caminfo = CamInfo()
   print("timelapse")
   try:
        return Response(gen_videos(caminfo.info["name"],0.5),
        mimetype='multipart/x-mixed-replace; boundary=frame')
   except Exception as ex:
        if state["Mode"].lower() == 'dashcam':
                write_state({"Mode":"off","current_file":"None"})
        print(ex)
        return "error "

led = 13
led_onof = lambda x: GPIO.output(led,x)

def setup_GPIO():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(led,GPIO.OUT)

try:
        print("starting")
        setup_GPIO()
        api = Api(app)
        caminfo = CamInfo()
        api.add_resource(CamInfo,'/info')
        print("added resource to rest")
        led_onof(1)
        app.run("0.0.0.0",port=caminfo.info['port'])
        led_onof(0)
except Exception as ex:
        led_onof(0)
        print(ex)
