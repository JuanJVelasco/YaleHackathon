from flask import Flask, Response, request, render_template, render_template_string
import cv2
import os
import datetime, time
import threading
import pyaudio
import wave

# audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512
RECORD_SECONDS = 15
WAVE_OUTPUT_FILENAME = "recordedFile.wav"
device_index = 2
audio = pyaudio.PyAudio()
audio_


# global varaibles

capture = False
rec = False
out = None
img = None

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300

camera = cv2.VideoCapture(0)

frame_width = int(camera.get(3))
frame_height = int(camera.get(4))
size = (frame_width, frame_height)

os.makedirs('./shots', exist_ok=True)
os.makedirs('./clips', exist_ok=True)

def gen_frames():
    global capture
    global img
    
    print('[DEBUG] gen_frames: start')

    while True:
        success, img = camera.read()
        
        if not success:
            break
        
        if capture:
            capture = False

            now = datetime.datetime.now()
            filename = "shot_{}.png".format(str(now).replace(":",''))
            path = os.path.sep.join(['shots', filename])

            print('[DEBUG] capture:', path)

            cv2.imwrite(path, img)

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    #return render_template('index.html')
    return render_template_string('''
Go to <a href="/requests">FORM</a>
''')

# define class only once
class TimerClass(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def run(self):
        seconds_10 = datetime.timedelta(seconds=10)
        
        while rec and not self.event.is_set():
            now = datetime.datetime.now()
            filename = "vid_{}.mp4".format(str(now).replace(":", ''))
            path = os.path.sep.join(['clips', filename])
            
            fourcc = cv2.VideoWriter_fourcc(*'MP4V')
            out = cv2.VideoWriter(path, fourcc, 25.0, size)

            end = now + seconds_10
            
            print('[DEBUG] end:', end)
            
            while now < end and rec and not self.event.is_set():
                if img is not None:  # `img` can be `numpy.array` so it can't check `if img:`
                    out.write(img)
                time.sleep(0.03)  # 1s / 25fps = 0.04  # it needs some time for code.
                now = datetime.datetime.now()
        
            # create mp4 file
            out.release()
            
    def stop(self):
        self.event.set()

@app.route('/requests', methods=['POST', 'GET'])
def tasks():
    global capture
    global rec
    
    print('[DEBUG] click:', request.form.get('click'))
    print('[DEBUG] rec  :', request.form.get('rec'))
    
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            capture = True

        if request.form.get('rec') == 'Start/Stop Recording':
            rec = not rec
    
            tmr = TimerClass()
    
            if rec:
                print("start")
                tmr.start()
            else:
                print("stop")
                tmr.stop()
    
    #return render_template_string('index.html')
    return render_template_string('''
        <img src="/video_feed"><br/>
        <form method="POST">
        <button type="submit" name="rec" value="Start/Stop Recording">Start/Stop Recording</button>
        </form>
        ''')

if __name__ == '__main__':
    thread_cam = threading.Thread(target=gen_frames)
    thread_cam.start()
    app.run(host='0.0.0.0', threaded=True, debug=True)