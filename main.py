from flask import Flask, render_template, request, session, redirect, url_for
import cv2
import numpy as np
import json
from urllib.request import urlopen
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vk0984242@gmail.com'
app.config['MAIL_PASSWORD'] = 'yqvj rilf eftl rhso'

mail = Mail(app)

users = {
    "Vish": {"password": "Vish@18"}
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('upload'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('upload'))
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        f = request.files['file']
        f.save('uploaded_video.mp4')
        return redirect(url_for('process_video'))
    return render_template('upload.html')

@app.route('/process_video')
def process_video():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Load Yolo
    net = cv2.dnn.readNet("yolov3_training_2000.weights", "yolov3_testing.cfg")
    classes = ["Weapon"]
    output_layer_names = net.getUnconnectedOutLayersNames()
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    cap = cv2.VideoCapture('uploaded_video.mp4')
    weapon_detected = False

    while True:
        ret, img = cap.read()
        if not ret:
            break

        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layer_names)

        # Showing information on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        if len(indexes) > 0:
            weapon_detected = True
            print("Weapon detected in frame")
            url = 'http://ipinfo.io/json'
            response = urlopen(url)
            data = json.load(response)

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            detection_info = {
                "ip": data['ip'],
                "city": data['city'],
                "region": data['region'],
                "country": data['country'],
                "location": data['loc'],
                "postal_code": data['postal'],
                "organization": data['org'],
                "timezone": data['timezone'],
                "current_time": current_time  # Add current time to detection_info
            }

            # Send email notification
            msg = Message('Weapon Detection Alert', sender='vk0984242@gmail.com', recipients=['visharad.baderao@mitaoe.ac.in'])
            msg.body = f"Weapon detected in uploaded video:\n\n" \
                       f"Location: {detection_info['location']}\n" \
                       f"City: {detection_info['city']}\n" \
                       f"Region: {detection_info['region']}\n" \
                       f"Country: {detection_info['country']}\n" \
                       f"Postal Code: {detection_info['postal_code']}\n" \
                       f"Organization: {detection_info['organization']}\n" \
                       f"Timezone: {detection_info['timezone']}\n" \
                       f"IP Address: {detection_info['ip']}\n" \
                       f"Current Time: {detection_info['current_time']}"

            mail.send(msg)

            break

    cap.release()
    cv2.destroyAllWindows()

    if weapon_detected:
        return render_template('result.html', detection_info=detection_info)
    else:
        return "Weapon not detected in the uploaded video."

if __name__ == "__main__":
    app.run(debug=True)
