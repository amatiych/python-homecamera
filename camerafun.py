"""
    camera functions
"""
import picamera
import io
from datetime import datetime
import time
from fractions import Fraction
import os


def capture_ex(fun):
        def wrapper(*args, **kwargs):
                try:
                        return fun(*args,**kwargs)
                except Exception as ex:
                        print(ex)
        return wrapper

def sorted_ls(path):
        mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
        return list(sorted(os.listdir(path), key=mtime))

def getfiles(path):
        files = [file for file in sorted_ls(path) if "h264" in file]
        return files

def get_file_name(files_to_keep,home):
        while True:
                files = getfiles(home)
                n = len(files)
                if n == files_to_keep:
                        oldest = files[0]
                        print("removing " + oldest)
                        os.remove(os.path.join(home,oldest))
                filename = datetime.now().strftime("%Y%m%d_%H%M%s.h264")
                yield os.path.join(home,filename)

def dashcam(length, files):
        folder = "/home/pi/Documents/python/homecamera"
        for filename in get_file_name(files,home=folder):

                with picamera.PiCamera() as cam:
                        try:
                                print("recording " + filename)
                                cam.start_recording(filename)
                                cam.wait_recording(length)
                                cam.stop_recording()
                        except Exception as ex:
                                print(ex)


def gen_videos(name,mult):
        stream = io.BytesIO()
        w = int(640 * mult)
        h = int(480 * mult)
        with picamera.PiCamera(resolution=(w,h)) as camera:
                camera.annotate_text_size = int(20*mult)
                camera.vflip = True
                camera.hflip = True
                #camera.frame_rate = 10
                for _ in camera.capture_continuous(stream,format='jpeg',use_video_port=True):
                        time.sleep(0.5)
                        camera.annotate_text = name + ' ' + time.ctime()
                        frame = stream.getvalue()
                        stream.truncate()
                        stream.seek(0)
                        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@capture_ex
def capture_picture(name, scale):
        print(str.format("capture picture  {0}:{1}", name, scale))
        ext = "camera:"
        w = int(640 * scale)
        h = int(480 * scale)
        print(str.format("capture picture  {0}:{1}", w,h))
        stream = io.BytesIO()
        stream.seek(0)
        with picamera.PiCamera(resolution=(w,h)) as camera:

                camera.start_preview()
                #camera.exposure_mode  ='night'
                camera.annotate_text = name +' ' + time.ctime()
                camera.vflip = True
                camera.hflip = True
                camera.annotate_text_size = int(20 * scale)
                camera.capture(stream,format="png")

                frame = stream.getvalue()

        return (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
	capture_picture('foo.jpg',0.5)




