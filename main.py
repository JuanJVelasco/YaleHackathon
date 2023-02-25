from flask import Flask, render_template, request, Response
import cv2

app = Flask(__name__, template_folder='static')

video = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('main.html', video_feed=gen(video))

def gen(video):
    while True:
        success, image = video.read()
        image = cv2.flip(image, 1)
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2204, threaded=True, debug=True)