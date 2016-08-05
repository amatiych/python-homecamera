import io
import re
from core import capture_ex
import os
import time
import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Response
import picamera
# This is the version to use dashcam static file

from  flask_restful import Resource, Api
from camerafun import capture_picture, gen_videos
# create our little application :)
app = Flask(__name__)

jsfile = "/home/pi/Documents/python/homecamera/camstate.json"

class CamInfo(Resource):

        def __init__ (self):
                filename = "/home/pi/features.json"
                with open(filename,'r') as f:
                        self.info = json.load(f)
                print(self.info)

        def __str__(self):
                return self.info
        def get(self):
                return self.info


@capture_ex
@app.route("/")
def home(index=0):
   caminfo = CamInfo()
   try:
       files = []
       videos = [f for f in os.listdir("/home/pi/Documents/videos/") if 'mp4' in f]
       for v in sorted(videos):
                th = re.sub("mp4","jpg",v)
                th = re.sub("_lock","",th)
                files.append((v,th))
       return render_template("/camera.html",port=caminfo.info['port'],files = files)
   except Exception as ex:
       print(ex)

@app.route("/video/<target>")
def video(target):
   print("in view for target %s " % target)
   #return "ok"
   return render_template("/show.html",target=target)


if __name__ == '__main__':

	try:
        	api = Api(app)
        	caminfo = CamInfo()
        	api.add_resource(CamInfo,'/info')
        	app.run("0.0.0.0",port=caminfo.info['port'])
	except Exception as ex:
        	print(ex)
