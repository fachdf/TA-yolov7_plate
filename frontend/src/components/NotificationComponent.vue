<template>
  <v-card height="auto">
    <!-- <v-icon icon="mdi-alert"></v-icon> -->
    <v-card-title>{{ notification.PelatNomor }}</v-card-title>
    <v-card-text>
      <!-- <p>ID Mahasiswa: {{ notification.IDMahasiswa}}</p> -->
      <p>RFID: {{ notification.RFID }}</p>
      <P>Waktu Akses: {{ notification.WaktuAkses }}</P> 
      <p>
        Bukti Akses Gagal: 
        <v-btn color="primary" rounded @click="openDialog(notification.BuktiAkses)">
          Lihat Gambar
        </v-btn>
      </p>
      <p>
        Bukti Akses Masuk: 
        <v-btn color="primary" rounded @click="openDialog(notification.BuktiMasuk)">
          Lihat Gambar
        </v-btn>
      </p>
      <p>Keterangan: {{ notification.Keterangan }}</p>
    </v-card-text>
    <v-card-actions>
      <v-dialog v-model="dialogVisible" persistent width="auto">
        <v-img :src="popupLink" width="100%"></v-img>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="closeDialog">Tutup</v-btn>
        </v-card-actions>
      </v-dialog>
      <v-dialog v-model="showKeteranganDialog" max-width="500px">
      <v-card>
        <v-card-title>Keterangan</v-card-title>
        <v-card-text>
          {{this.keterangan}}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="closeKeteranganDialog">Tutup</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
      <v-btn color="success" class="ma-2 mt-4 white--text" @click="postDataIzinkan" large>
        <v-icon right dark class="mr-2">
          mdi-check
        </v-icon>
        Izinkan
      </v-btn>

      <v-btn color="red" class="ma-2 mt-4 white--text" @click="postDataTolak" large outlined>
        <v-icon right dark class="mr-2">
          mdi-close
        </v-icon>
        Tolak
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
  
<script>

import axios from 'axios';


export default {
  data() {
    return {
      showKeteranganDialog: false,
      dialogVisible: false,
      popupLink: '',
      keterangan :''
    }
  },
  props: {
    notification: {
      type: Object,
      required: true,
    },
  },
  methods:{
    async postDataIzinkan() {
      await axios({
        method: 'post',
        url: 'http://localhost:8080/update_mhs_izinkan_keluar',
        data: {
          mhs_id: this.notification.IDMahasiswa,
          bukti_akses_gagal: this.notification.BuktiAkses
        }
      })
      .then(response =>{
        this.localnotification = response.data.data
      })
      .catch(error => {
        console.log(error.request.response)
      })
      
      this.openKeteranganDialog("Mahasiswa diizinkan untuk keluar.");
  },

    async postDataTolak() {
      try {
        await axios({
          method: 'post',
          url: 'http://localhost:8080/update_mhs_tolak_keluar',
          data: {
            mhs_id: this.notification.IDMahasiswa,
            keterangan_tolak: this.keteranganTolak, // Tambahkan keterangan tolak ke dalam data yang dikirim
          },
        });
        // ...
      } catch (error) {
        console.log(error.request.response);
      }
      
      this.openKeteranganDialog("Mahasiswa ditolak untuk keluar.");
    },

    openDialog(item) {
      this.popupLink = item;
      this.dialogVisible = true;
    },
    
    closeDialog() {
      this.dialogVisible = false;
      this.popupLink = '';
    },

    openKeteranganDialog(ket) {
      this.keterangan = ket
      this.showKeteranganDialog = true;
    },
    closeKeteranganDialog() {
      this.showKeteranganDialog = false;
      this.keteranganTolak = ''; // Reset keterangan tolak setelah ditutup
    },
  }
  
};
</script>

<style scoped>
</style>