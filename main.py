from flask import Flask, render_template, request, Response
import cv2
import time
import moviepy.editor as mp

app = Flask(__name__, template_folder='static')

video = cv2.VideoCapture(0)



def grab_latest_file(dir): #grab latest file from directory
    pass

@app.route('/')
def index():
    return render_template('main.html', video_feed=gen(video))

def gen(video):
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640,480))

    t_end = time.time() + 30
    while time.time() < t_end:
        success, image = video.read()
        image = cv2.flip(image, 1)
        ret, jpeg = cv2.imencode('.jpg', image)
        out.write(image)
        frame = jpeg.tobytes()
        # print("recording frame")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        

    # end camera and build mp4
    video.release()
    out.release()
    cv2.destroyAllWindows()

    print("created video file")

    # build mp3 file
    # clip = mp.VideoFileClip(r"media/mp4/output.mp4")
    # print(clip)

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2204, threaded=True, debug=True)
    
