import psycopg2
from datetime import datetime
from sshtunnel import SSHTunnelForwarder


# Fungsi untuk etry data pengendara masuk ; return id
def add_mhs_masuk(rfid, pelat, status):
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()

        pelat = pelat.replace(" ", "")  # Remove all spaces

        # Execute the SQL query to insert the text into the database
        #cur.execute("INSERT INTO pengendara (user_rfid, user_pelat, user_status) VALUES (%s, %s, %s)", (rfid ,pelat, 0))
        
        #new_id = cur.fetchone()[0]
        #print(new_id)

        sql = "INSERT INTO pengendara (user_rfid, user_pelat, user_status) VALUES (%s, %s, %s) RETURNING user_id;"
        data = (rfid, pelat, status)
        cur.execute(sql, data)
        new_id = cur.fetchone()[0]
        
        # Commit the transaction
        sql2 = "INSERT INTO kendaraan (kendaraan_pelat, user_user_id) VALUES (%s, %s);"
        
        data2 = (pelat, new_id)
        cur.execute(sql2, data2)
        # Close the cursor and connection objects
        conn.commit()
        cur.close()
        conn.close()
        
        
        # Return a success message
        return new_id
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        if conn:
         conn.rollback()
        return f"Error while saving new user to database: {error}"

# Entry data pengendara gagal masuk/keluar
# Fungsi untuk mengubah status mhs setelah keluar (0 = masuk, 1 = keluar, 2 = gagal scan) ; return id
def update_mhs_keluar(rfid, status):
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()

        # Execute the SQL query to insert the text into the database
        #cur.execute("INSERT INTO pengendara (user_rfid, user_pelat, user_status) VALUES (%s, %s, %s)", (rfid ,pelat, 0))
        
        #new_id = cur.fetchone()[0]
        #print(new_id)
        sql = "UPDATE pengendara SET user_status = %s WHERE user_rfid = %s AND user_status IN (%s,%s) RETURNING user_id"
        print(sql)
        data = (status, rfid, 0,2)
        cur.execute(sql, data)
        userid = cur.fetchone()[0]
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        
        # Return a success message
        return userid
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return None

# Fungsi untuk menambahkan pengendara keluar namun rfid belum pernah digunakan untuk masuk

def get_mhs_data_by_rfid(rfid):
    try:
        # establish a connection to the database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )

        # create a cursor object
        cur = conn.cursor()
        
        # execute the SELECT query to retrieve RFID and Plat Nomor data from gateparking table
        cur.execute("SELECT user_id, user_rfid, user_pelat FROM pengendara WHERE user_rfid = %s AND user_status IN (%s, %s)", (rfid, 0,2))
        
        # fetch all the rows from the result set
        rows = cur.fetchall()

        # return the retrieved data
        if len(rows) > 0:
            #print(len(rows))
            return rows
        else:
            return None
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
        
    finally:
        # close the cursor and connection objects
        cur.close()
        conn.close()

def get_mhs_data_by_pelat(pelat):
    try:
        # establish a connection to the database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )

        # create a cursor object
        cur = conn.cursor()
        
        # execute the SELECT query to retrieve RFID and Plat Nomor data from gateparking table
        cur.execute("SELECT user_id, user_rfid, user_pelat FROM pengendara WHERE user_pelat = %s AND user_status = %s", (pelat, 0))
        
        # fetch all the rows from the result set
        rows = cur.fetchall()

        # return the retrieved data
        if len(rows) > 0:
            #print(len(rows))
            return rows
        else:
            return None
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
        
    finally:
        # close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()

def get_mhs_data_by_id(id):
    try:
        # establish a connection to the database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )

        # create a cursor object
        cur = conn.cursor()
        
        # execute the SELECT query to retrieve RFID and Plat Nomor data from gateparking table
        cur.execute("SELECT user_id, user_rfid, user_pelat FROM pengendara WHERE user_id = %s AND user_status = 0", (id))
        
        # fetch all the rows from the result set
        rows = cur.fetchall()

        # return the retrieved data
        return rows
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
        
    finally:
        # close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()

# Get data mhs by pelat nomor 
def get_mhs_data_by_pelat(pelat):
    try:
        # establish a connection to the database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )

        # create a cursor object
        cur = conn.cursor()
        
        # execute the SELECT query to retrieve RFID and Plat Nomor data from gateparking table
        cur.execute("SELECT user_id, user_rfid, user_pelat FROM pengendara WHERE user_pelat = %s AND user_status = %s", (pelat, 0))
        
        # fetch all the rows from the result set
        rows = cur.fetchall()

        # return the retrieved data
        if len(rows) > 0:
            #print(len(rows))
            return rows
        else:
            return None
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
        
    finally:
        # close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()

# Fungsi untuk menambahkan waktu masuk dan bukti masuk
def add_riwayat_masuk_with_bukti(bukti_masuk, id_mhs):
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()
        
        now = datetime.now(now) # Create timestamp

        # Execute the SQL query to insert the text into the database
        cur.execute("INSERT INTO riwayat (bukti_akses, waktu_akses, user_user_id) VALUES (%s, %s, %s)", (bukti_masuk, now, id_mhs))
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return "Mhs and Riwayat saved to database successfully"
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

# Menambah riwayat masuk hanya id tanpa bukti
def add_riwayat_masuk(id_mhs, keterangan):
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()
        
        now = datetime.now() # Create timestamp

        # Execute the SQL query to insert the text into the database
        cur.execute("INSERT INTO riwayat (waktu_akses, user_user_id, keterangan, riwayat_type) VALUES (%s, %s, %s)", (now, id_mhs, keterangan))
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return keterangan
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

def add_riwayat_gagal(id_mhs, keterangan):
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()
        
        now = datetime.now() # Create timestamp

        # Execute the SQL query to insert the text into the database
        cur.execute("INSERT INTO riwayat (waktu_akses_gagal, user_user_id, keterangan) VALUES (%s, %s, %s)", (now, id_mhs, keterangan))
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return keterangan
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

def update_riwayat_gagal(id_mhs, keterangan):
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()
        
        now = datetime.now() # Create timestamp

        # Execute the SQL query to insert the text into the database
        cur.execute("UPDATE riwayat SET waktu_akses_gagal = %s, keterangan = %s WHERE user_user_id = %s", (now, keterangan, id_mhs ))
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return keterangan
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

#Update bukti masuk dari link cloudinary
def update_bukti_masuk(bukti_masuk, user_id):
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()

        # Execute the SQL query to insert the text into the database
        cur.execute("UPDATE riwayat SET bukti_masuk = %s WHERE user_user_id = %s", (bukti_masuk, user_id))
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return "Bukti masuk URL saved to database successfully"
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

def update_bukti_gagal(bukti_gagal, user_id):
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()

        # Execute the SQL query to insert the text into the database
        cur.execute("UPDATE riwayat SET bukti_akses_gagal = %s WHERE user_user_id = %s", (bukti_gagal, user_id))
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return "Bukti masuk URL saved to database successfully"
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

# Fungsi untuk menambahkan waktu keluar dan bukti keluar
def update_riwayat_keluar_with_bukti(bukti_keluar, user_id):
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()
        
        now = datetime.now() # Create timestamp

        # Execute the SQL query to insert the text into the database
        cur.execute("UPDATE riwayat SET bukti_keluar = %s, waktu_keluar = %s WHERE user_user_id = %s", (bukti_keluar, now, user_id))
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return "Mhs saved to database successfully"
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

# Update riwayat keluar tanpa bukti
def update_riwayat_keluar(user_id, keterangan):
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()
        
        now = datetime.now() # Create timestamp

        # Execute the SQL query to insert the text into the database
        cur.execute("UPDATE riwayat SET waktu_keluar = %s, keterangan = %s WHERE user_user_id = %s", (now, keterangan, user_id))
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return keterangan
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

# tambah bukti keluar
def update_bukti_keluar(bukti_keluar, user_id):
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()

        # Execute the SQL query to insert the text into the database
        cur.execute("UPDATE riwayat SET bukti_keluar = %s WHERE user_user_id = %s", (bukti_keluar, user_id))
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return "Bukti keluar URL saved to database successfully"
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"
###
def update_izinkan_keluar(bukti_keluar, user_id):
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        keterangan = "Diizinkan keluar oleh Petugas"
        # Create a cursor object
        cur = conn.cursor()

        now = datetime.now() 
        # Execute the SQL query to insert the text into the database
        cur.execute("UPDATE riwayat SET waktu_keluar = %s, bukti_keluar = %s, keterangan = %s WHERE user_user_id = %s", (now, bukti_keluar, keterangan, user_id))
        cur.execute("UPDATE pengendara SET user_status = %s WHERE user_id = %s", (1, user_id))
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return "Bukti keluar URL saved to database successfully"
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"
####
def update_tolak_keluar(user_id):
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        keterangan = "Tidak diizinkan untuk keluar oleh petugas"
        # Create a cursor object
        cur = conn.cursor()

        now = datetime.now() 
        # Execute the SQL query to insert the text into the database
        #cur.execute("UPDATE riwayat SET waktu_keluar = %s, bukti_keluar = %s WHERE user_user_id = %s", (now, bukti_keluar, user_id))
        #cur.execute("UPDATE pengendara SET user_status = %s WHERE user_id = %s", (2, user_id))
        cur.execute("UPDATE riwayat SET keterangan = %s WHERE user_user_id = %s", (keterangan, user_id))
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return "Bukti keluar URL saved to database successfully"
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"
####
def get_all_riwayat():
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()

        # Execute the SQL query to insert the text into the database
        cur.execute("SELECT rp.bukti_masuk, rp.waktu_masuk, rp.bukti_keluar, rp.waktu_keluar, rp.bukti_akses_gagal, rp.waktu_akses_gagal, m.user_pelat, m.user_rfid, m.user_status, rp.keterangan, m.user_id FROM riwayat rp JOIN pengendara m ON rp.user_user_id = m.user_id WHERE m.user_status IN (0,1,2)")
        
        # Commit the transaction
        rows = cur.fetchall()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return rows
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

def get_all_riwayat_gagal():
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()

        # Execute the SQL query to insert the text into the database
        cur.execute("SELECT rp.waktu_akses_gagal, rp.bukti_akses_gagal, m.user_pelat, m.user_rfid, m.user_status, rp.keterangan, m.user_id FROM riwayat rp JOIN pengendara m ON rp.user_user_id = m.user_id WHERE m.user_status = 3")
        
        # Commit the transaction
        rows = cur.fetchall()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return rows
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        if conn:
         conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

def get_all_peringatan_gagal():
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()

        # Execute the SQL query to insert the text into the database
        cur.execute("SELECT rp.waktu_akses_gagal, rp.bukti_akses_gagal, rp.waktu_masuk, rp.bukti_masuk, m.user_pelat, m.user_rfid, m.user_status, rp.keterangan, m.user_id FROM riwayat rp JOIN pengendara m ON rp.user_user_id = m.user_id WHERE m.user_status = 2")
        
        # Commit the transaction
        rows = cur.fetchall()
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        #server.stop()
        # Return a success message
        return rows
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

def get_jml_parkir():
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()
        
        now = datetime.now() # Create timestamp

        # Execute the SQL query to insert the text into the database
        cur.execute("SELECT COUNT(*) FROM pengendara WHERE user_status IN (0,1,2)")

        
        result = cur.fetchone()[0]
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

def get_jml_keluar_parkir():
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()
        
        now = datetime.now() # Create timestamp

        # Execute the SQL query to insert the text into the database
        cur.execute("SELECT COUNT(*) FROM pengendara WHERE user_status = 1")

        
        result = cur.fetchone()[0]
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return result
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

def get_jml_problem_parkir():
    try:
        # Connect to the PostgreSQL database
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()
        
        now = datetime.now() # Create timestamp

        # Execute the SQL query to insert the text into the database
        cur.execute("SELECT COUNT(*) FROM pengendara WHERE user_status = 2")

        
        result = cur.fetchone()[0]
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return result
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

def get_test():
    try:
        # Connect to the PostgreSQL database
        # server = SSHTunnelForwarder(('103.209.131.66', 8022),
        #  ssh_username='fachrid4',
        #  ssh_pkey='D:\\Download\\ssh\\id_rsa',
        #  remote_bind_address=('localhost', 5432),
        #  local_bind_address=('localhost', 5434))
        # server.start()
        # conn = psycopg2.connect(
        #     host= server.local_bind_host,
        #     port= server.local_bind_port,
        #     database="gateparking",
        #     user="pari",
        #     password="kota407"
        # )
        conn = psycopg2.connect(
            host= "localhost",
            port= "5432",
            database="gateparkingotomatis",
            user="postgres",
            password="postgres"
        )
        
        # Create a cursor object
        cur = conn.cursor()
        
        now = datetime.now() # Create timestamp

        # Execute the SQL query to insert the text into the database
        cur.execute("SELECT COUNT(*) FROM pengendara WHERE user_status = 1")

        
        result = cur.fetchone()[0]
        
        # Close the cursor and connection objects
        cur.close()
        cur.close()
        conn.close()
        
        # Return a success message
        return result
    
    except (Exception, psycopg2.DatabaseError) as error:
        # If an error occurs, rollback the transaction and return an error message
        conn.rollback()
        return f"Error while saving new riwayat to database: {error}"

def jaccard_similarity(str1, str2):
    length = max(len(str1), len(str2))
    print(length)
    diff_count = sum(c1 != c2 for c1, c2 in zip(str1, str2))
    print(diff_count)
    similarity_percentage = ((length - diff_count) / length) * 100
    return similarity_percentage



if __name__ == '__main__':
    #res = add_mhs(12345678901, "D 6280 SAG")]
    #res = update_mhs_keluar("12345678901", 1)
    #res = update_riwayat_keluar("bukti_keluar/1.jpg")
    # rfid = "12345678903"
    # res = get_mhs_data_by_rfid(rfid, "D6280SAG")
    #res = get_jml_parkir()
    #res =  get_mhs_data_by_rfid("2454076420")
    #res = update_bukti_keluar("https://res.cloudinary.com/jtk/image/upload/v1684497128/gwqd188isqicobc4yqc5.jpg", 52)
    #res = get_jml_problem_parkir()
    #res = add_mhs_masuk("test1", "test2", 0)
    #res = get_all_peringatan_gagal()
    #res = jaccard_similarity('AAAAAAAAAA', 'AAAAAAAAAB')
    #res2 = get_jml_keluar_parkir()
    res = get_test()
    #res = update_izinkan_keluar("test/test.jpg", 34)
    print(res)
    #print(res2)