from flask import Flask, request, jsonify
# import sys 
import base64
# sys.path.append('D:/TUGASAKHIR/Github/TA-yolov7_plate/YOLOv7/')
from postgresql_conn import *
import cv2
from identifikasi_plat import identifikasi_plat_nomor
import os
from datetime import datetime
import cloudinary
# import cloudinary.uploader
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
# cloudinary.config(
#   cloud_name = "jtk",
#   api_key = "256473613645129",
#   api_secret = "608g68rUKA13x6RFA3r5zfqVv5k"
# )


@app.route('/identifikasi_masuk', methods=['POST'])
#
# Requirement : Input = RFID & Gambar. => Identifikasi pelat nomor => Simpan di PostgreSQL (DONE)
#
def identifikasi_masuk():
    # Input RFID dan Gambar
    data = request.get_json()
    photo = data['photo']
    rfid = data['filename']
    now = datetime.now() 
    filename = rfid + now.strftime("-%H-%M-%S")
    # Decode base64 encoded image
    image_data = base64.b64decode(photo)
    # Save the image
    with open(f'data_riwayat/image_{filename}.jpg', 'wb') as f:
        f.write(image_data)
    bukti_masuk = "data_riwayat/image_" + filename + ".jpg"
    # Cek RFID sedang digunakan/tidak
    mhs =  get_mhs_data_by_rfid(rfid)
    # Identifikasi Pelat Nomor
    pelat = identifikasi_plat_nomor(bukti_masuk)  

    if mhs == None: # Jika RFID blm terdaftar
        if pelat != None: # Jika Pelat nomor terdeteksi
            is_pelat = get_mhs_data_by_pelat(pelat)
            if is_pelat == None: # Jika pelat nomor belum terdaftar
                # Berhasil masuk (RFID dan pelat nomor baru)
                status = 0
                id_mhs = add_mhs_masuk(rfid, pelat, status)
                #result = add_riwayat_masuk_with_bukti(bukti_masuk, id_mhs)
                keterangan = "Berhasil masuk."
                result = add_riwayat_masuk(id_mhs, keterangan)
                code = 200
                keterangan = result
                #return jsonify({'message': result, 'code': code, 'user_id' : id_mhs})
            else: # Error Jika pelat telah terdaftar masuk ke sistem
                status = 3
                id_mhs = add_mhs_masuk(rfid, pelat, status)
                keterangan = "Pelat telah terdaftar"
                result = add_riwayat_gagal(id_mhs, keterangan)
                code = 500
                keterangan = result
                #return jsonify({'message': keterangan, 'code': code, 'user_id' : id_mhs})
        else: # Pelat tidak terdeteksi : HARUS ULANGI
            keterangan = "RFID OK, Pelat tidak terdeteksi"
            code = 504
            #keterangan = result
            id_mhs = None

    else: # RFID telah tersimpan di database dan sedang parkir
        status = 3 
        if pelat == None:
            pelat = ""
        id_mhs = add_mhs_masuk(rfid, pelat, status)
        keterangan = "RFID telah dipakai."
        code = 501
        result = add_riwayat_gagal(id_mhs, keterangan)
        keterangan = result

    os.remove(bukti_masuk) 
    return jsonify({'message': keterangan, 'code' : code, 'user_id' : id_mhs})   

@app.route('/identifikasi_keluar', methods=['POST'])
#
# Requirement : Input = RFID & Gambar. => Identifikasi pelat nomor => Cocokkan dengan yang ada di PostgreSQL
#
def identifikasi_keluar():
    # Input RFID dan Gambar
    data = request.get_json()
    photo = data['photo']
    rfid = data['filename']
    now = datetime.now() 
    filename = rfid + now.strftime("-%H-%M-%S")
    # Decode base64 encoded image
    image_data = base64.b64decode(photo)
    # Save the image
    with open(f'data_riwayat/image_{filename}.jpg', 'wb') as f:
        f.write(image_data)
    
    # Identifikasi Pelat Nomor
    bukti_keluar = "data_riwayat/image_" + filename + ".jpg"
    mhs =  get_mhs_data_by_rfid(rfid)
    pelat = identifikasi_plat_nomor(bukti_keluar)
    if mhs != None: # Jika ada mhs di database dengan RFID tsb
        print("###############DATA MAHASISWA##################")
        print(mhs)
        pelat_nomor_terdaftar = mhs[0][2]
        if pelat != None: # Kalo plat terdeteksi
            if pelat_nomor_terdaftar == pelat: # Jika pelat nomor sama dengan mhs terdaftar dengan RFID input
                status = 1
                id_mhs = update_mhs_keluar(rfid, status)
                code = 200
                keterangan = "Berhasil keluar."
                result = update_riwayat_keluar(id_mhs, keterangan)
                os.remove(bukti_keluar)
                return jsonify({'message': result, 'code': code, 'user_id' : id_mhs})
            else: # Kalo pelat beda : Simpan dgn status 2
                status = 2
                keterangan = "Pelat nomor berbeda dengan Data Masuk"
                id_mhs = update_mhs_keluar(rfid, status)
                result = update_riwayat_gagal(id_mhs, keterangan)
                code = 501
        else : # Pelat tidak terdeteksi : HARUS ULANGI HINGGA TERDETEKSI
            keterangan = "Pelat tidak terdeteksi"
            code = 504
            #keterangan = result
            id_mhs = None
    else: # Jika tdk ada mhs dengan RFID tersebut
        if pelat != None: #Jika pelat nomor terdeteksi
            # Kalo plat terdeteksi ; cari apakah pelat sama dengan pelat seorang mahasiswa?
            mhs = get_mhs_data_by_pelat(pelat)
            if mhs != None: # Jika pelat nomor ada di data mhs yang parkir
                pelat_nomor_terdaftar = mhs[0][2]
                status = 2 
                rfid = mhs[0][0]
                id_mhs = update_mhs_keluar(rfid, status)
                code = 505 # RFID beda tp pelat ada
                keterangan = "Pelat Kendaraan Terdaftar namun RFID berbeda"
                #result = update_riwayat_keluar_with_bukti(bukti_keluar, id_mhs)
                print(id_mhs)
                result = add_riwayat_gagal(id_mhs, keterangan)
            else: # Kalo pelat beda & RFID beda
                status = 3
                id_mhs = add_mhs_masuk(rfid, status)
                keterangan = "RFID dan Pelat Nomor tidak terdaftar"
                result = add_riwayat_gagal(id_mhs, keterangan)
                code = 501 # RFID Beda pelat tidak ada
                
        else : # Pelat tidak terdeteksi = ULANG
            os.remove(bukti_keluar)
            result = "Error pelat tidak terdeteksi"
            code = 504
            id_mhs = None

    os.remove(bukti_keluar) 
    return jsonify({'message': keterangan, 'code' : code, 'user_id' : id_mhs})   

@app.route('/get_riwayat_parkir', methods=['GET'])
#
# Requirement : Input = - 
#               Output = Record riwayat parkir
# 
def get_riwayat_parkir():
    data = get_all_riwayat_parkir()
    return data

# Get riwayat  with status 2-3
@app.route('/get_riwayat_gagal', methods=['GET'])
#
# Requirement : Input = - 
#               Output = Record riwayat parkir
# 
def get_riwayat_gagal():
    data = get_all_riwayat_gagal()
    return data


# Get riwayat  with status 2
@app.route('/get_peringatan_gagal', methods=['GET'])
#
# Requirement : Input = - 
#               Output = Record riwayat parkir
# 
def get_peringatan_gagal():
    data = get_all_peringatan_gagal()
    return data

@app.route('/get_riwayat_count', methods=['GET'])
#
# Requirement : Input = - 
#               Output = Record riwayat parkir
# 
def get_riwayat_count():
    data = get_jml_parkir()
    return jsonify({'data': data})

@app.route('/get_keluar_count', methods=['GET'])
#
# Requirement : Input = - 
#               Output = Record riwayat parkir
# 
def get_keluar_count():
    data = get_jml_keluar_parkir()
    return jsonify({'data': data})

@app.route('/get_problem_count', methods=['GET'])
#
# Requirement : Input = - 
#               Output = Record riwayat parkir
# 
def get_problem_count():
    data = get_jml_problem_parkir()
    return jsonify({'data': data})

# Update riwayat untuk menambahkan bukti masuk
@app.route('/update_bukti_masuk', methods=['POST'])
def update_mhs_bukti_masuk():
    data = request.get_json()
    bukti_masuk = data['bukti_masuk']
    user_id = data['user_id']
    print("data:")
    print(bukti_masuk)
    print(user_id)
    return update_bukti_masuk(bukti_masuk, user_id)

# Update riwayat untuk menambahkan bukti keluar
@app.route('/update_bukti_keluar', methods=['POST'])
def update_mhs_bukti_keluar():
    data = request.get_json()
    bukti_keluar = data['bukti_keluar']
    user_id = data['user_id']
    print("data:")
    print(bukti_keluar)
    print(user_id)
    return update_bukti_keluar(bukti_keluar, user_id)

# Update riwayat untuk menambahkan bukti gagal
@app.route('/update_bukti_gagal', methods=['POST'])
def update_mhs_bukti_gagal():
    data = request.get_json()
    bukti_gagal = data['bukti_gagal']
    user_id = data['user_id']
    print("data:")
    print(bukti_gagal)
    print(user_id)
    return update_bukti_gagal(bukti_gagal, user_id)


if __name__ == '__main__':
    app.run(debug=True, port=8099, host=0.0.0.0)