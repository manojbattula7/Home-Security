from flask import Flask, Response, render_template, request, redirect, url_for,send_from_directory,send_file, session
import cv2
import os
import sqlite3
import tensorflow as tf
import numpy as np
from fire_detection import fire_detection1
from faceattendence import face_attendance
# from violence_detection import violence_detection1
# from cleaning_detection import cleaning_detection
# from staff_cleaning import cleaning_det
# ection_staff
from urllib.parse import quote_plus
import face_recognition 
# from activity_tracking import activity_track

# Configure TensorFlow to use GPU if available

physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
else:
    print("No GPU found")

def gen_frames(camera):
    print(camera)
    cap=cv2.VideoCapture(camera)
    while True:
        success, frame = cap.read()  # Read frame from the camera
        if not success:
            break
        else:
            frame = cv2.resize(frame, (640, 480))
            #FaceRecognition().encode_faces()
            #frame = FaceRecognition().process_frame(frame)  # Process frame with face recognition
            # frame=activity_track(frame)
           # frame=cleaning_detection_staff(frame,"camera3","living room")
            # Perform fire detection and take appropriate action
            frame = fire_detection1(frame, "Camera1", "Living Room")  # Assuming camera name and room name
            frame = face_attendance(frame)
            #frame=violence_detection1(frame,"Camera3","Living Room")
            #frame=cleaning_detection(frame,"Camera4","Kitchen")


            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Concat frame one by one and show result
            


def get_csv_files():
    csv_files = []
    for file in os.listdir('csv_folder'):
        if file.endswith('.csv'):
            csv_files.append(file)
    return csv_files

def get_video_folders():
    video_folders = [folder for folder in os.listdir('video_folder') if os.path.isdir(os.path.join('video_folder', folder))]
    return video_folders

# Function to create a connection to the SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('security_system.sqlite')
    except sqlite3.Error as e:
        print(e)
    return conn

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'


@app.route('/')
def home():
    return render_template('index.html')

# Route for login
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Create a connection to the database
        conn = create_connection()
        if conn is not None:
            try:
                # Query the database to fetch the user with the provided username
                c = conn.cursor()
                c.execute("SELECT * FROM Users WHERE Email=?", (username,))
                user = c.fetchone()
                print(user[5])
                if user and user[5] == password:  # user[3] is the password column
                    # Redirect to a dashboard or home page on successful login
                    session['email'] = username
                    print(username)
                    return redirect(url_for('dashboard'))
                else:
                    error = 'Invalid credentials. Please try again.'
            except sqlite3.Error as e:
                print(e)
                error = 'Error accessing the database.'
            finally:
                conn.close()
        else:
            error = 'Database connection error.'

    return render_template('login.html', error=error)


# Route for signing up
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    error = None

    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        password = request.form['password']

        # Create a connection to the database
        conn = create_connection()
        if conn is not None:
            try:
                # Insert user details into the database
                c = conn.cursor()
                c.execute("INSERT INTO users (email, name, address,phone, password) VALUES (?, ?,?,?, ?)", (email, name, address,phone, password))
                conn.commit()
                conn.close()
                return redirect(url_for('dashboard'))
            except sqlite3.Error as e:
                print(e)
                error = 'Error inserting user details into the database.'
        else:
            error = 'Database connection error.'

    return render_template('signup.html', error=error)

# Dummy route for the dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/devices_add', methods=['GET', 'POST'])
def devices_add():
    if request.method == 'POST':
        room_name = request.form['RoomName']
        device_name = request.form['DeviceName']
        device_address = request.form['DeviceAddress']
        port_number = request.form['PortNumber']
        channel = request.form['Channel']

        # Connect to the database
        conn = sqlite3.connect('security_system.sqlite')
        c = conn.cursor()

        # Insert the data into the database
        c.execute("INSERT INTO Devices (RoomName, DeviceName, deviceaddress, portnumber, channel) VALUES (?, ?, ?, ?, ?)",
                  (room_name, device_name, device_address, port_number, channel))
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return redirect(url_for('devices_list'))

    return render_template('devices_add.html')


# Route to display all devices and delete option
@app.route('/devices_list')
def devices_list():
    # Connect to the database
    conn = sqlite3.connect('security_system.sqlite')
    c = conn.cursor()

    # Retrieve all devices from the database
    c.execute("SELECT * FROM devices")
    devices = c.fetchall()

    # Close the connection
    conn.close()

    return render_template('devices_list.html', devices=devices)

# Route to delete a device
@app.route('/delete_device/<int:id>', methods=['POST'])
def delete_device(id):
    # Connect to the database
    conn = sqlite3.connect('security_system.sqlite')
    c = conn.cursor()

    # Delete the device with the given id
    c.execute("DELETE FROM devices WHERE DeviceID=?", (id,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return redirect(url_for('devices_list'))


@app.route('/settings')
def settings():
    return render_template('setting.html')


@app.route('/aboutus')
def aboutus():
    return render_template('about.html')

@app.route('/update')
def update():
    return render_template('update.html')

# Route for logging out
@app.route('/logout')
def logout():
    # Remove the email from the session if it's there
    session.pop('email', None)
    # Redirect to the home page after logout
    return redirect(url_for('login'))

@app.route('/editprofile')
def editprofile():
    # Get the logged-in user's email from session
    logged_in_email = session.get('email')
    print(logged_in_email)
    # Create a connection to the database
    conn = create_connection()
    if conn is not None:
        try:
            # Query the database to fetch the user data
            c = conn.cursor()
            c.execute("SELECT * FROM Users WHERE Email=?", (logged_in_email,))
            print(c)
            user_data = c.fetchone()  # Fetch user data
            print(user_data)
            if user_data:
                # Extract user details
                user_id, name, email, address, phone, password = user_data[0],user_data[1],user_data[2],user_data[3],user_data[4],user_data[5]
                return render_template('edit_profile.html', name=name, email=email, address=address, phone=phone,password=password)
            else:
                return "User not found."
        except sqlite3.Error as e:
            print(e)
            return "Error accessing the database."
        finally:
            conn.close()
    else:
        return "Database connection error."


@app.route('/edit_user_details', methods=['POST'])
def edit_user_details():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        phone = request.form['phone']

        # Create a connection to the database
        conn = create_connection()
        if conn is not None:
            try:
                # Update user details in the database
                c = conn.cursor()
                c.execute("UPDATE Users SET Name=?, Address=?, Phone=?, Password=? WHERE Email=?", (name, address, phone, password, email))
                conn.commit()
                conn.close()
                return redirect(url_for('settings'))
            except sqlite3.Error as e:
                print(e)
                return "Error updating user details."
        else:
            return "Database connection error."
    else:
        return "Method not allowed."



@app.route('/update_password', methods=['POST'])
def update_password():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['new-password']

        # Create a connection to the database
        conn = create_connection()
        if conn is not None:
            try:
                # Update user details in the database
                c = conn.cursor()
                c.execute("UPDATE Users SET Password=? WHERE Email=?", ( password, email))
                conn.commit()
                conn.close()
                return redirect(url_for('login'))
            except sqlite3.Error as e:
                print(e)
                return "Error updating user details."
        else:
            return "Database connection error."
    else:
        return "Method not allowed."



@app.route('/camera_view')
def camera_view():
    # Connect to the database
    conn = create_connection()
    if conn is not None:
        try:
            # Fetch camera details from the database
            c = conn.cursor()
            c.execute("SELECT * FROM Devices")
            cameras = c.fetchall()
            return render_template('camera_view.html', cameras=cameras)
        except sqlite3.Error as e:
            print(e)
            return "Error accessing the database."
        finally:
            conn.close()
    else:
        return "Database connection error."



@app.route('/event')
def index():
    folder1_path = 'video_folder'
    folder2_path = 'csv_folder'

    folder1_contents = os.listdir(folder1_path)
    folder2_contents = os.listdir(folder2_path)
    return render_template('event.html', folder1_contents=folder1_contents, folder2_contents=folder2_contents)

@app.route('/videos/<filename>')
def video_view(filename):
    folder1_path = 'video_folder'
    return send_from_directory(folder1_path, filename)

@app.route('/csv/<filename>')
def csv_view(filename):
    folder2_path = 'csv_folder'
    filepath = os.path.join(folder2_path, filename)
    return send_file(filepath, as_attachment=False, mimetype='text/csv')



@app.route('/video_feed/<string:deviceaddress>')
def video_feed(deviceaddress):
    if deviceaddress=='0':
        deviceaddress1=int(deviceaddress)
        return Response(gen_frames(deviceaddress1), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response(gen_frames(deviceaddress), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.config['SECRET_KEY'] = '7f19f15d88598da137f26f4fccb798fafa7959feb7a26002'
    app.run(debug=True)
