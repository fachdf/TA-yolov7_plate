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
    </v-card-title>

    <v-tabs v-model="selectedTab" class="pl-4" fixed-tabs color="orange">
      <v-tab v-for="(tab, index) in tabs" :key="index">
        {{ tab.title }}
      </v-tab>
    </v-tabs>
    

    <v-tabs-items v-model="selectedTab" class="left-side">
      <v-tab-item v-for="(tab, index) in tabs" :key="index">
        <v-col 
        sm="5"
        md="6"
        mr=auto 
        >
          <v-text-field
          max-width="344"
          class="left-input pt-4 pl-4 pr-4 mx-auto"
          v-model="tab.search"
          append-icon="mdi-magnify"
          label="Filter Status"
          outlined
          dense
          ></v-text-field>
        </v-col>
        
        <v-data-table 
        :headers="tab.headers" 
        :items="getFilteredItems(index)" 
        :items-per-page="rows"
        :sort-by.sync="tab.sortBy"
        :sort-desc.sync="tab.sortAsc"
        class="elevation-1 pl-4 pr-4">
        <template v-slot:[`item.BuktiMasuk`]="{ item }">
          <v-btn color="primary" rounded @click="openDialog(item.BuktiMasuk)">
            Lihat Bukti
          </v-btn>
        </template>
        <template v-slot:[`item.BuktiKeluar`]="{item}">
          <v-btn color="orange" rounded @click="openDialog(item.BuktiKeluar)">
            Lihat Bukti
          </v-btn>
        </template>
        <template v-slot:[`item.BuktiAkses1`]="{item}">
          <v-btn color="orange" rounded @click="openDialog(item.BuktiAkses1)">
            Lihat Bukti
          </v-btn>
        </template>
      </v-data-table>
      <v-dialog v-model="dialogVisible" persistent width="auto">
        <v-img :src="popupLink" width="100%"></v-img>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="closeDialog">Tutup</v-btn>
        </v-card-actions>
      </v-dialog>
      </v-tab-item>
    </v-tabs-items>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'
export default {
  name: 'riwayat-page',
  data() {
      return {
        tabs: [
          {
            title: 'Riwayat Parkir', 
            headers: [{
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
            { text: 'Status', value: 'Status', sortable: false },
            { text: 'Keterangan', value: 'Keterangan', sortable: false },
            ],
            data: [],
            search: '',
            filteredData:[],
            sortBy: 'WaktuMasuk',
            sortAsc: false,
          },
          {
            title: 'Riwayat Akses', 
            headers: [{
              text: 'RFID',
              align: 'start',
              sortable: false,
              value: 'RFID1',
            },
            // { text: 'ID Mahasiswa', value: 'IDMahasiswa1' },
            { text: 'Pelat Nomor', value: 'PelatNomor1', sortable: false, },
            { text: 'Waktu Akses', value: 'WaktuAkses1' },
            { text: 'Bukti Akses', value: 'BuktiAkses1', sortable: false, },
            { text: 'Status', value: 'Status1', sortable: false, },
            { text: 'Keterangan', value: 'Keterangan1', sortable: false, },
            ],
            data: [],
            search:'',
            filteredData:[],
            sortBy: 'WaktuAkses1',
            sortAsc: false,
          }
        ],
        dialogVisible: false,
        popupLink: '',
        rows: 10,
        selectedTab: 0,
      }
    },

    mounted() {
      this.getDataRiwayat();
      setInterval(this.getDataRiwayat,3000);
    },

    methods: {
      async getDataRiwayat() {
        try {
          const response1 = await axios.get('http://192.168.34.201:8090/get_riwayat_parkir'); // Ganti '/api/endpoint' dengan URL API yang sesuai
          const list = response1.data
          const mappedRiwayat = list.map((item) => ({
            BuktiKeluar: item[2],
            BuktiMasuk: item[0],
            PelatNomor: item[4],
            RFID: item[5],
            Status: item[6],
            WaktuKeluar: item[3],
            WaktuMasuk: item[1],
            Keterangan: item[7]
          }));
          this.tabs[0].data = mappedRiwayat
          this.tabs[0].sortDesc = false

          const response2 = await axios.get('http://192.168.34.201:8090/get_peringatan_gagal'); // Ganti '/api/endpoint' dengan URL API yang sesuai
          const list1 = response2.data
          const mappedRiwayatAkses = list1.map((item) => ({
            BuktiAkses1: item[0],
            WaktuAkses1: item[1],
            PelatNomor1: item[2],
            RFID1: item[3],
            Status1: item[4],
            Keterangan1: item[5],
            IDMahasiswa1: item[6]
          }));
          this.tabs[1].data = mappedRiwayatAkses
          this.tabs[1].sortDesc = false

          console.log(response1)
          console.log(response2)
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

      getFilteredItems(index) {
        if (index === 0) {
          return this.filteredData1;
        } else if (index === 1) {
          return this.filteredData2;
        }
        return [];
      }
    },

    computed: {
      filteredData1() {
        if (!this.tabs[0].search) {
          return this.tabs[0].data;
        }

        const searchKeyword = parseInt(this.tabs[0].search);

        return this.tabs[0].data.filter(item => {
          const status = item.Status;

          return status == searchKeyword;
        });
     },

      filteredData2() {
        if (!this.tabs[1].search) {
          return this.tabs[1].data;
        }

        const searchKeyword = parseInt(this.tabs[1].search);

        return this.tabs[1].data.filter(item => {
          const status = item.Status1;

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

.left-input input{
  text-align: left;
}
</style>