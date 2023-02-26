from flask import Flask, Response, request, render_template, render_template_string
import cv2
import pyaudio
import wave
import datetime, time
import os
from threading import Thread

app = Flask(__name__)

# camera = cv2.VideoCapture(0)

# frame_width = int(camera.get(3))
# frame_height = int(camera.get(4))
# size = (frame_width, frame_height)



# global varaibles
capture = False
rec = False
out = None
img = None

now = datetime.datetime.now()

# def gen_frames():
#     global capture
#     global img
    
#     print('[DEBUG] gen_frames: start')

#     while True:
#         success, img = camera.read()
        
#         if not success:
#             break
        
#         if capture:
#             capture = False

#             now = datetime.datetime.now()
#             filename = "shot_{}.png".format(str(now).replace(":",''))
#             path = os.path.sep.join(['shots', filename])

#             print('[DEBUG] capture:', path)

#             cv2.imwrite(path, img)

#         frame = cv2.imencode('.jpg', img)[1].tobytes()
        
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# def start():
#     now = datetime.datetime.now()

#     filename = "vid_{}.mp4".format(str(now).replace(":", ''))
#     path = os.path.sep.join(['clips',filename])
    
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(path, fourcc, 25.0, size)

#     stream = audio.open(format=FORMAT, channels=CHANNELS,
#         rate=RATE, input=True,input_device_index = 0,
#         frames_per_buffer=CHUNK)
#     print ("recording started")
#     Recordframes = []
#     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#         data = stream.read(CHUNK)
#         Recordframes.append(data)
#         out.write(img)

#     out.release()
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()
     
#     waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#     waveFile.setnchannels(CHANNELS)
#     waveFile.setsampwidth(audio.get_sample_size(FORMAT))
#     waveFile.setframerate(RATE)
#     waveFile.writeframes(b''.join(Recordframes))
#     waveFile.close()

def record_video():
    # print("VIDEO")

    # fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    # out = cv2.VideoWriter('tester.mp4', fourcc, 20.0, (640,480))

    # t_end = time.time() + 15
    # while time.time() < t_end:
    #     success, image = camera.read()
    #     image = cv2.flip(image, 1)
    #     ret, jpeg = cv2.imencode('.jpg', image)
    #     if ret:
    #         out.write(img)
    #         frame = jpeg.tobytes()

    # camera.release()
    # out.release()
    # cv2.destroyAllWindows()
    cap = cv2.VideoCapture(0)


    # Get video metadata
    video_fps = cap.get(cv2.CAP_PROP_FPS),
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)


    # we are using x264 codec for mp4
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # writer = cv2.VideoWriter('OUTPUT_PATH.mp4', apiPreference=0, fourcc=fourcc,fps=video_fps[0], frameSize=(int(width), int(height)))
    writer = cv2.VideoWriter('output2023.mp4',fourcc, 15, (int(cap.get(3)),int(cap.get(4))))

    t_end = time.time() + 15
    while time.time() < t_end:
        ret, frame = cap.read()
        if not ret: break # break if cannot receive frame
        # convert to grayscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        writer.write(frame) # write frame
        
        if cv2.waitKey(1) & 0xFF == ord('q'): # on press of q break
            break

    print("DONE RECORDING VIDEO")
        
    # release and destroy windows
    writer.release()
    cap.release()
    cv2.destroyAllWindows()

def record_audio():
    print("AUDIO")

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    RECORD_SECONDS = 15
    WAVE_OUTPUT_FILENAME = f'{now}.wav'
    device_index = 2
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,input_device_index = 0,
                frames_per_buffer=CHUNK)
    print ("recording started")
    Recordframes = []
     
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        Recordframes.append(data)
    print ("recording stopped")
     
    stream.stop_stream()
    stream.close()
    audio.terminate()
     
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()

@app.route('/record', methods=['POST', 'GET'])
def record():
    t1 = Thread(target = record_video)
    t2 = Thread(target = record_audio)

    t1.start()
    t2.start()

    return "recorded"

@app.route('/test', methods=['POST'])
def test():
    # global rec
    # if request.method == 'POST':
    #     if request.form.get('click') == 'Capture':
    #         capture = True

    #     if request.form.get('rec') == 'Start/Stop Recording':
    #         rec = not rec
    
    #         # tmr = TimerClass()
    
    #         if rec:
    #             print("start")
    #             # tmr.start()
    #             start()
    #         else:
    #             print("stop")
    #             # tmr.stop()

    return render_template_string('''
        <img src="/video_feed"><br/>
        <form method="POST">
        <button type="submit" name="rec" value="Start/Stop Recording">Start/Stop Recording</button>
        </form>
        ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)