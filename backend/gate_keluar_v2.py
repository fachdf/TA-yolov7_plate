import cv2
import base64
import tkinter as tk
from PIL import Image, ImageTk
from detect_rec_plate_custom import main
import time
import requests,json
import cloudinary
import cloudinary.uploader
import io
import os 

url_deploy = 'http://127.0.0.1:6009/'
#url_deploy = 'https://gpujtk.polban.studio/'

def upload_file(filename):

  cloudinary.config(
    cloud_name = "jtk",
    api_key = "256473613645129",
    api_secret = "608g68rUKA13x6RFA3r5zfqVv5k"
  )
  image = Image.open(filename)
  with io.BytesIO() as output:
        image.save(output, format='JPEG')
        image_data = output.getvalue()
  response = cloudinary.uploader.upload(image_data)
  return response['url']

def capture_photo():
    # Open default camera
    cap = cv2.VideoCapture(0)

    # Check if the camera was opened successfully
    if not cap.isOpened():
        print("Error opening video capture device")
        return

    # Capture the photo
    ret, frame = cap.read()

    # Release the camera
    cap.release()

    # Check if the photo was captured successfully
    if not ret:
        print("Error capturing photo")
        return

    # Save the photo to disk
    filename = "photo.jpg"
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 1)
    cv2.imwrite(filename, frame)
    # Save the photo to a file
    # Read the image file as bytes
    with open(filename, 'rb') as f:
        encoded_image = base64.b64encode(f.read())

    # Set the API endpoint URL
    url = url_deploy+'identifikasi_keluar'

    # Set the request headers
    headers = {"Content-Type": "image/jpeg"}
    
    data = {
        'photo': encoded_image.decode('utf-8'),
        'filename': number
    }


    response = requests.post(url, json=data)
    response = json.loads(response.text)
    # Send the request
    #response = requests.post(url, data=image_data, headers=headers)
    print(response)
    #response['code'] == 200
    # =200
    code = response['code']
    if(code == 200):
        #print(response['user_id'])
        #print("ini urlnya: " + upload_file(filename))
        data_bukti = {
            'bukti_keluar' : upload_file(filename),
            'user_id' : response['user_id']
            #'user_id' : 54
        }
        url_bukti = url_deploy+'update_bukti_keluar'
        response = requests.post(url_bukti, json=data_bukti)
    elif(code == 504):
        print("Silahkan ulangi")
    else:
        #print(response['user_id'])
        #print("ini urlnya: " + upload_file(filename))
        data_bukti = {
            'bukti_gagal' : upload_file(filename),
            'user_id' : response['user_id']
            #'user_id' : 54
        }
        url_bukti = url_deploy+'update_bukti_gagal'
        response = requests.post(url_bukti, json=data_bukti)
    os.remove(filename)

# Main loop
while True:
    # Output Voice : Suara "Silahkan Tap Kartu"
    user_input = input("Enter a number (x to exit): ")

    # Exit the program if the user enters 0
    if user_input == "x":
        break

    # Capture a photo if the user enters a number
    try:
        number = (user_input)
        capture_photo()
        time.sleep(2)
    except Exception as error:
        print(error)