import cv2
import base64
from PIL import Image, ImageTk
from detect_rec_plate_custom import main
import time
import requests,json
import cloudinary
import cloudinary.uploader
import io
import os 
from datetime import datetime
import playsound

url_deploy = 'http://localhost:8099/'
#url_deploy = 'https://gpujtk.polban.studio/'
#url_deploy = 'http://localhost:8099/'
def upload_file(filename):
  print("Uploading...")
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
  print("Masuk sini sih")
  print(response['url'])
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
    #frame = cv2.flip(frame, 1)
    
    # Save the photo to a file
    cv2.imwrite(filename, frame)

    # Read the image file as bytes
    with open(filename, 'rb') as f:
        encoded_image = base64.b64encode(f.read())

    # Set the API endpoint URL
    url = url_deploy+'identifikasi_masuk'

    # Set the request headers
    headers = {'Content-Type': 'application/json'}
    
    data = {
         "photo": encoded_image.decode('utf-8'),
         "filename": number
    }
    now = datetime.now()
    response = requests.post(url, json.dumps(data), headers=headers)
    response = json.loads(response.text)
    then = datetime.now()
    code = response['code']
    # Send the request
    #response = requests.post(url, data=image_data, headers=headers)
    print("Time : ")
    print(then-now)
    if(code == 500):
        playsound.playsound('sound\\500.mp3', True) 
    elif(code == 501):
        playsound.playsound('sound\\501.mp3', True)
    elif(code == 502):
        playsound.playsound('sound\\502.mp3', True)
    elif(code == 503):
        playsound.playsound('sound\\503.mp3', True)
    elif(code == 504):
        playsound.playsound('sound\\504.mp3', True)
    elif(code == 505):
        playsound.playsound('sound\\505.mp3', True)
    elif(code == 506):
        playsound.playsound('sound\\506.mp3', True)  
    elif(code == 200):
        playsound.playsound('sound\\200_01.mp3', True)  

    print(response['message'])
    print(response['code'])
    # code = response['code']
    if(code == 200):
        data_bukti = {
            'bukti_masuk' : upload_file(filename),
            'user_id' : response['user_id']
        }
        url_bukti = url_deploy + 'update_bukti_masuk'
        response = requests.post(url_bukti, json=data_bukti)
    elif(code == 504):
        print("Silahkan ulangi")
    else:
        data_bukti = {
            'bukti_gagal' : upload_file(filename),
            'user_id' : response['user_id']
        }
        url_bukti = url_deploy + 'update_bukti_gagal'
        response = requests.post(url_bukti, json=data_bukti)

    
   #os.remove(filename)

# Main loop
while True:
    # Get input from the user
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

# RFID test = 12345678901

