<template>
  <v-container class="grey lighten-5">
    <v-card
    class="left-side"
    outlined
    tile
    >
      <v-card-title class="title">
          Riwayat Pengguna Gedung Parkir Politeknik Negeri Bandung
        <v-spacer></v-spacer>
        <v-text-field
          class="pt-4"
          v-model="search"
          append-icon="mdi-magnify"
          label="Filter Status"
          outlined
          dense
        ></v-text-field>
      </v-card-title>
      <v-data-table
      :headers="headers"
      :items="filteredData"
      :items-per-page="rows"
      class="elevation-1 pl-4 pr-4"
      >
        <template v-slot:[`item.BuktiMasuk`]="{ item }">
          <v-btn color="primary" rounded @click="openDialog(item.BuktiMasuk)">
            Lihat Bukti
          </v-btn>
        </template>
        <template v-slot:[`item.BuktiKeluar`]="{item}">
          <v-btn color="primary" rounded @click="openDialog(item.BuktiKeluar)">
            Lihat Bukti
          </v-btn>
        </template>
      </v-data-table>
      <v-dialog v-model="dialogVisible"  persistent width="auto">
        <v-img :src="popupLink" width="100%"></v-img>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="closeDialog">Tutup</v-btn>
        </v-card-actions>
      </v-dialog>
      <v-card-text>
        <p class="text-h6" color="orange"> Keterangan Status</p>
        <p>
          0 = Mahasiswa masih didalam area parkir 
          <br> 
          1 = Mahasiswa sudah keluar area parkir
          <br>
          2 = Mahasiswa masih didalam area parkir (masalah)
        </p>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'
export default {
  name: 'riwayat-page',
  data() {
      return {
        headers: [
          {
            text: 'RFID',
            align: 'start',
            sortable: false,
            value: 'RFID',
          },
          { text: 'Pelat Nomor', value: 'PelatNomor', sortable: false, },
          { text: 'Waktu Masuk', value: 'WaktuMasuk' },
          { text: 'Bukti Masuk', value: 'BuktiMasuk', sortable: false, },
          { text: 'Waktu Keluar', value: 'WaktuKeluar' },
          { text: 'Bukti Keluar', value: 'BuktiKeluar', sortable: false, },
          { text: 'Status', value: 'Status', sortable: false, },
        ],
        items: [],
        search: '',
        dialogVisible: false,
        popupLink: '',
        rows: 10
      }
    },

    mounted() {
      //this.getDataRiwayat();
      //setInterval(this.getDataRiwayat,3000);
    },

    methods: {
      async getDataRiwayat() {
        try {
          const response = await axios.get('http://localhost:8080/get_riwayat_parkir'); // Ganti '/api/endpoint' dengan URL API yang sesuai
          // this.items = response.data;
          const list = response.data
          const mappedRiwayat = list.map((item) => ({
            BuktiKeluar: item[2],
            BuktiMasuk: item[0],
            PelatNomor: item[4],
            RFID: item[5],
            Status: item[6],
            WaktuKeluar: item[3],
            WaktuMasuk: item[1],
          }));
          this.items = mappedRiwayat
          console.log(response)
        } catch (error) {
          console.error(error);
        }
      },
      openDialog(item) {
        this.popupLink = item;
        this.dialogVisible = true;
      },
      closeDialog() {
        this.dialogVisible = false;
        this.popupLink = '';
      },
    },

    computed: {
      filteredData() {
        if (!this.search) {
          return this.items;
        }

        const searchKeyword = parseInt(this.search);

        return this.items.filter(item => {
          // Sesuaikan dengan properti atau kolom "status" yang ingin Anda filter
          const status = item.Status;

          // Kembalikan item yang memenuhi kondisi pencarian
          return status == searchKeyword;
        });
      }
    }
}
</script>

<style scoped>
.title{
color: orange;
font-display: bold;
}
.left-side{
text-align: left;
margin-top: 0px;
}
</style>