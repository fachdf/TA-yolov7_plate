import cv2
import base64
import tkinter as tk
from PIL import Image, ImageTk
from detect_rec_plate_custom import main
import argparse
import requests,json

# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Create the GUI window
root = tk.Tk()
root.title("Scan Plat Nomor")
status = False
def on_key_press(event):
    global status
    number = entry.get()
    if status == False:
        capture_photo(number)
    else:
        print("processing")
# Define a function to capture a photo
def capture_photo(number):
    global status
    if (len(number) >= 10) and (status == False):
        print("Masuk")
        status = True
        #Read a frame from the video stream
        entry.delete(0, 10)
        entry.pack_forget()
        ret, frame = cap.read()
        # Convert the frame to RGB format
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert the frame to a PIL ImageTk object
        frame = cv2.flip(frame, 1)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image)
        # Display the photo in a label
        label.config(image=photo)
        label.image = photo
        # Save the photo to a file
        cv2.imwrite("imgs/photo_temp.jpg", frame)
        # Read the image file as bytes
        with open('imgs/photo_temp.jpg', 'rb') as f:
            encoded_image = base64.b64encode(f.read())

        # Set the API endpoint URL
        url = 'http://127.0.0.1:5000/identifikasi_masuk'

        # Set the request headers
        headers = {"Content-Type": "image/jpeg"}
        
        data = {
            'photo': encoded_image.decode('utf-8'),
            'filename': number
        }


        response = requests.post(url, json=data)

        # Send the request
        #response = requests.post(url, data=image_data, headers=headers)
        print(response.text)
        root.after(5000,entry.pack)
        status = False
    elif status == True:
        print("Still processing")

#Namespace(detect_model=['weights/yolov7-lite-s.pt'], rec_model='weights/plate_rec.pth', source='imgs', img_size=640, output='result', kpt_label=4)
# Create a label to display the video stream
label = tk.Label(root)
label.pack()
label2 = tk.Label(root, text="Enter a 12 digit number:")
label2.pack()
entry = tk.Entry(root)
entry.pack()
entry.bind('<KeyRelease>', on_key_press)
# Create a button to capture a photo
button = tk.Button(root, text="Capture Photo", command=capture_photo)
button.pack()
# Start the GUI main loop
while True:
    #Read a frame from the video stream
    ret, frame = cap.read()
    #Convert the frame to RGB format
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 1)
    # Convert the frame to a PIL ImageTk object
    image = Image.fromarray(frame)
    photo = ImageTk.PhotoImage(image)
    # Display the photo in a label
    label.config(image=photo)
    label.image = photo
    # Update the GUI window
    root.update()