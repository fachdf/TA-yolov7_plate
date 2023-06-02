import cv2
import tkinter as tk
from PIL import Image, ImageTk
from detect_rec_plate_custom import main
import argparse


# Define a function to capture a photo
def identifikasi_plat_nomor(photo):
    try:

        opt = argparse.Namespace()
        opt.detect_model = 'weights/best_v2.pt'
        opt.rec_model = 'weights/plate_rec.pth'
        opt.source = photo
        opt.img_size = 640
        opt.output = 'result'
        opt.kpt_label = 4
        plat_nomor = main(opt)
        if plat_nomor:
            return plat_nomor
        else:
            return None
    except (Exception) as error:
        print(error)
        return None
# RFID test = 1234567890
# if __name__ == '__main__':
#     #print(identifikasi_plat_nomor('https://res.cloudinary.com/jtk/image/upload/v1683964619/zuyfmjcg8wnzhfphmfuj.jpg'))