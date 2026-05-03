import os
import cv2
import datetime
import face_recognition
import numpy as np
from flask import Flask, render_template_string, Response, jsonify
from openpyxl import Workbook, load_workbook
import threading

app = Flask(__name__)

# ------------------- Load Student Images -------------------
path = "Students"
images, student_names = [], []
for file in os.listdir(path):
    img = cv2.imread(os.path.join(path, file))
    if img is not None:
        images.append(img)
        student_names.append(os.path.splitext(file)[0])

def encode_faces(images):
    encodings = []
    for img in images:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(rgb)
        if encode:
            encodings.append(encode[0]) 
    return encodings

encoded_list = encode_faces(images)
print("Encoding Complete")

# ------------------- Excel Setup -------------------
folder = "Attendance_Records"
if not os.path.exists(folder):
    os.mkdir(folder)

def create_daily_file():
    today = datetime.date.today().strftime("%Y-%m-%d")
    file_path = os.path.join(folder, f"{today}.xlsx")

    if not os.path.exists(file_path):
        wb = Workbook()
        ws = wb.active
        ws.title = "Attendance"
        ws.append(["Name", "Status", "Entry Time"])  # Header

        # Default all students Absent
        for name in student_names:
            ws.append([name.upper(), "Absent", "-", "-"])

        wb.save(file_path)
    return file_path

# ------------------- Attendance Function -------------------
def mark_attendance(name, fixed_leave=None):
    file_path = create_daily_file()
    wb = load_workbook(file_path)
    ws = wb.active

    for row in ws.iter_rows(min_row=2):  # skip header
        if row[0].value == name:
            current_time = datetime.datetime.now().strftime("%H:%M")

            entry_times = [] if row[2].value == "-" else row[2].value.split(", ")
            # leave_times = [1] if row[3].value == "-" else row[3].value.split(", ")

            if row[1].value == "Absent":
                row[1].value = "Present"
                entry_times.append(current_time)
                row[2].value = ", ".join(entry_times)
                # row[3].value = "-" if not leave_times else ", ".join(leave_times)
            # else:
            #     if fixed_leave:
                    # leave_times.append(fixed_leave)
                # else:
                #     leave_times.append(current_time )
                # row[3].value = ", ".join(leave_times)

            wb.save(file_path)
            print(f"Updated record for {name}")
            return

    wb.save(file_path)

# ------------------- Camera Control -------------------
cap = None
stop_flag = True
lock = threading.Lock()

def open_camera():
    global cap
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)

def close_camera():
    global cap
    if cap is not None:
        cap.release()
        cap = None

def gen_frames():
    global cap, stop_flag
    open_camera()

    while True:
        with lock:
            if stop_flag:
                break
        success, frame = cap.read()
        if not success:
            break
        else:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces_current = face_recognition.face_locations(rgb_frame)
            encodes_current = face_recognition.face_encodings(rgb_frame, faces_current)

            for encodeFace, faceLoc in zip(encodes_current, faces_current):
                matches = face_recognition.compare_faces(encoded_list, encodeFace)
                faceDis = face_recognition.face_distance(encoded_list, encodeFace)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = student_names[matchIndex].upper()
                    y1, x2, y2, x1 = faceLoc
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX,
                                0.9, (0, 255, 0), 2)
                    mark_attendance(name)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    close_camera()
    cv2.destroyAllWindows()

# ------------------- API Routes -------------------
@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Face Recognition Attendance</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background: #f8f9fa;
                font-family: Arial, sans-serif;
                padding: 30px;
            }
            .card {
                border-radius: 15px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            .btn {
                border-radius: 30px;
                font-size: 16px;
                padding: 10px 20px;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2 class="text-primary">📸 Face Recognition Attendance System</h2>
                <p class="text-muted">Mark attendance automatically using your face.</p>
            </div>

            <div class="card p-4 mb-4">
                <h5>Camera Control</h5>
                <div class="d-flex gap-3 mt-3">
                    <a href="/start" class="btn btn-success">▶ Start Camera</a>
                    <a href="/stop" class="btn btn-danger">⏹ Stop Camera</a>
                </div>
            </div>

            <div class="card p-4 mb-4">
                <h5>Attendance Records</h5>
                <div class="d-flex gap-3 mt-3">
                    <a href="/attendance" class="btn btn-info text-white">📊 View Attendance</a>
                    <a href="/api/attendance" class="btn btn-dark">⚡ Get Attendance (JSON)</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route('/start')
def start():
    global stop_flag
    with lock:
        stop_flag = False
    # Directly show video in iframe
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Camera Started</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { text-align:center; padding:20px; background:#f8f9fa; }
            iframe { width:80%; height:500px; border-radius:15px; border:2px solid #000; margin-top:20px; }
        </style>
    </head>
    <body>
        <h3 class="text-success">✅ Camera Started Successfully!</h3>
        <p>Live video stream is running below 👇</p>
        <iframe src="/video"></iframe>
        <br><br>
        <a href='/stop' class="btn btn-danger">⏹ Stop Camera</a>
        <a href='/' class="btn btn-secondary">⬅ Back to Home</a>
    </body>
    </html>
    """
    return html


@app.route('/stop')
def stop():
    global stop_flag
    with lock:
        stop_flag = True
    return """
    <div style="font-family:Arial; text-align:center; padding:40px;">
        <h3 style="color:red;">⏹ Camera stopped successfully!</h3>
        <a href='/' class="btn btn-secondary">⬅ Back</a>
    </div>
    """


@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/attendance')
def show_attendance():
    file_path = create_daily_file()
    wb = load_workbook(file_path)
    ws = wb.active

    data = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        data.append(row)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="10">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { padding:30px; background:#f8f9fa; }
            .table { border-radius:10px; overflow:hidden; }
        </style>
    </head>
    <body>
        <h2 class="mb-4 text-primary">📊 Attendance Record</h2>
        <p class="text-muted">Auto-refresh every 10 seconds</p>
        <table class="table table-bordered table-striped">
            <thead class="table-dark">
                <tr>
                    <th>Name</th>
                    <th>Status</th>
                    <th>Entry Time(s)</th>
                </tr>
            </thead>
            <tbody>
                {% for row in data %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>
                        {% if row[1] == 'Present' %}
                            <span class="badge bg-success">{{ row[1] }}</span>
                        {% else %}
                            <span class="badge bg-danger">{{ row[1] }}</span>
                        {% endif %}
                    </td>
                    <td>{{ row[2] }}</td>

                </tr>
                {% endfor %}
            </tbody>
        </table>
        <a href="/" class="btn btn-secondary">⬅ Back to Home</a>
    </body>
    </html>
    """
    return render_template_string(html, data=data)


@app.route('/api/attendance')
def api_attendance():
    file_path = create_daily_file()
    wb = load_workbook(file_path)
    ws = wb.active

    data = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        data.append({"Name": row[0], "Status": row[1], "Entry": row[2], "Leave": row[3]})
    return jsonify(data)

# ------------------- Run App -------------------
if __name__ == "__main__":
    create_daily_file()
    app.run(host="0.0.0.0", port=5000, debug=True)
