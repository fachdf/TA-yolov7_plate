<template>
  <v-card height="auto">
    <!-- <v-icon icon="mdi-alert"></v-icon> -->
    <v-card-title>{{ notification.PelatNomor }}</v-card-title>
    <v-card-text>
      <!-- <p>ID Mahasiswa: {{ notification.IDMahasiswa}}</p> -->
      <p>RFID: {{ notification.RFID }}</p>
      <P>Waktu Akses: {{ notification.WaktuAkses }}</P> 
      <p>
        Bukti Akses: 
        <v-btn color="primary" rounded @click="openDialog(notification.BuktiAkses)">
          Lihat Bukti
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
        url: 'http://localhost:8099/update_mhs_izinkan_keluar',
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
  },

    async postDataTolak() {
      await axios({
        method: 'post',
        url: 'http://localhost:8099/update_mhs_izinkan_keluar',
        data: {
          mhs_id: this.notification.IDMahasiswa,
        }
      })
      .then(response =>{
        this.localnotification = response.data.data
      })
      .catch(error => {
        console.log(error.request.response)
      })
    },

    openDialog(item) {
      this.popupLink = item;
      this.dialogVisible = true;
    },
    closeDialog() {
      this.dialogVisible = false;
      this.popupLink = '';
    },
  }
  
};
</script>

<style scoped>
</style>