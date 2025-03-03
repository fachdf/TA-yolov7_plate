import cv2
import tkinter as tk
from PIL import Image, ImageTk
from detect_rec_plate_custom import main
import argparse


# Define a function to capture a photo
def identifikasi_plat_nomor(photo):
    try:

        opt = argparse.Namespace()
        opt.detect_model = 'weights/last_v2.pt'
        opt.rec_model = 'weights/plate_rec.pth'
        opt.source = photo
        #opt.source = 'data_riwayat/image_070709986564-17-19-26.jpg'
        opt.img_size = 640
        opt.output = 'result'
        opt.kpt_label = 4
        plat_nomor = main(opt)
        print("plat nomor type data:")
        print(type(plat_nomor))
        if plat_nomor:
            if(type(plat_nomor) == str):
                return plat_nomor
            elif(type(plat_nomor) == list):
                return plat_nomor[0]['plate_no']
        else:
            return None
    except (Exception) as error:
        print(error)
        return None
# RFID test = 1234567890
# if __name__ == '__main__':
#     #print(identifikasi_plat_nomor('https://res.cloudinary.com/jtk/image/upload/v1683964619/zuyfmjcg8wnzhfphmfuj.jpg'))

if __name__ == '__main__':
    #identifikasi_plat_nomor("data_riwayat/image_070709986564-17-19-26.jpg")
    identifikasi_plat_nomor()