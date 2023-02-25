import numpy as np
import cv2


roi_x, roi_y, roi_w, roi_h = 100, 100, 200, 200

def extract_green(frame):
    return frame[:,:,1]

def perform_fft(signal):
    return np.abs(np.fft.rfft(signal))

cap = cv2.VideoCapture(0)

prev_mean = 0
prev_max = 0
threshold = 20

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    green_channel = extract_green(frame)
    
    roi = green_channel[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
    
    fft = perform_fft(roi)

    max_freq = np.argmax(fft)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    bpm = (max_freq * fps * 60 / roi_w)/100
    
    mean_amp = np.mean(fft)
    max_amp = np.max(fft)
    if (max_amp - prev_max) > threshold and prev_mean != 0 and mean_amp > prev_mean:
        print("Pulse detected!")
    
    prev_mean = mean_amp
    prev_max = max_amp
    
    cv2.putText(frame, f"BPM: {bpm:.0f}", (roi_x, roi_y-10), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 3)
    
    cv2.imshow("rPPG", frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



