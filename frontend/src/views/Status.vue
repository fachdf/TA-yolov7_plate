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

    <v-tabs v-model="selectedTab" class="pl-4" fixed-tabs color="#FB9503">
      <v-tab v-for="(tab, index) in tabs" :key="index">
        {{ tab.title }}
      </v-tab>
    </v-tabs>
    
    <v-tabs-items v-model="selectedTab" class="left-side">
      <v-tab-item v-for="(tab, index) in tabs" :key="index">
      <v-row>
        <v-col 
        sm="5"
        md="6"
        mr=auto 
        >
          <v-select
          max-width="344"
          class="pt-4 pl-4 mx-auto"
          v-model="tab.selectedTimeFilter"
          :items="tab.timeFilterOptions"
          label="Filter Waktu"
          outlined
          dense
          ></v-select>
        </v-col>

        <v-col
        sm="5"
        offset-sm="2"
        md="6"
        offset-md="0"
        >
          <v-select v-if="index === 0"
          max-width="344"
          class="left-input pt-4 pr-4 mx-auto"
          v-model="tab.selectedFilter"
          :items="tab.filterOptions"
          label="Filter Status"
          outlined
          dense
          ></v-select>
        </v-col>
      </v-row>  
        <v-data-table 
        :headers="tab.headers" 
        :items="getFilteredItems(index)" 
        :items-per-page="rows"
        :sort-by.sync="tab.sortBy"
        :sort-desc.sync="tab.sortDesc"
        class="elevation-1 pl-4 pr-4">
          <template v-slot:[`item.BuktiMasuk`]="{ item }">
            <v-btn color="primary" rounded @click="openDialog(item.BuktiMasuk)" :disabled=!item.BuktiMasuk>
              Lihat
            </v-btn>
          </template>
          <template v-slot:[`item.BuktiKeluar`]="{item}">
            <v-btn color="primary" rounded @click="openDialog(item.BuktiKeluar)" :disabled=!item.BuktiKeluar>
              Lihat
            </v-btn>
          </template>
          <template v-slot:[`item.BuktiAkses`]="{item}">
            <v-btn color="primary" rounded @click="openDialog(item.BuktiKeluar)" :disabled=!item.BuktiAkses>
              Lihat
            </v-btn>
          </template>
          <template v-slot:[`item.BuktiAkses1`]="{item}">
            <v-btn color="primary" rounded @click="openDialog(item.BuktiAkses1)" :disabled=!item.BuktiAkses1>
              Lihat
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
import moment from 'moment';
import 'moment-timezone';

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
            { text: 'Waktu Akses Terakhir', value: 'WaktuAkses' },
            { text: 'Bukti Akses Terakhir', value: 'BuktiAkses', sortable: false, },
            { text: 'Status', value: 'Status'},
            { text: 'Keterangan', value: 'Keterangan', sortable: false },
            ],
            data: [],
            selectedFilter: null,
            filterOptions: ['Semua', 'Masih Didalam', 'Telah Keluar', 'Bermasalah'],
            timeFilterOptions: ['Semua', 'Hari ini', 'Kemarin'],
            filteredData:[],
            sortBy: 'WaktuMasuk',
            sortDesc: false,
            selectedTimeFilter: null,
          },
          {
            title: 'Riwayat Akses', 
            headers: [{
              text: 'RFID',
              align: 'start',
              sortable: false,
              value: 'RFID1',
            },
            { text: 'Pelat Nomor', value: 'PelatNomor1', sortable: false, },
            { text: 'Waktu Akses', value: 'WaktuAkses1' },
            { text: 'Bukti Akses', value: 'BuktiAkses1', sortable: false, },
            { text: 'Status', value: 'Status1', sortable: false, },
            { text: 'Keterangan', value: 'Keterangan1', sortable: false, },
            ],
            data: [],
            timeFilterOptions: ['Semua', 'Hari ini', 'Kemarin'],
            filteredData:[],
            sortBy: 'WaktuAkses1',
            sortDesc: false,
            selectedTimeFilter: null,
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
          const response1 = await axios.get('http://192.168.34.201:8099/get_riwayat_parkir'); // Ganti '/api/endpoint' dengan URL API yang sesuai
          const list = response1.data 
          const mappedRiwayat = list.map((item) => {
            const waktuKeluar = moment(item[3]);
            const waktuMasuk = moment(item[1]);
            const waktuAkses = moment(item[5]);

            return {
              BuktiMasuk: item[0],
              WaktuMasuk: waktuMasuk.isValid() ? waktuMasuk.tz('Asia/Jakarta').format('YYYY-MM-DD HH:mm:ss') : "No Data",
              BuktiKeluar: item[2],
              WaktuKeluar: waktuKeluar.isValid() ? waktuKeluar.tz('Asia/Jakarta').format('YYYY-MM-DD HH:mm:ss') : "No Data",
              BuktiAkses: item[4],
              WaktuAkses: waktuAkses.isValid() ? waktuKeluar.tz('Asia/Jakarta').format('YYYY-MM-DD HH:mm:ss') : "No Data",
              
              PelatNomor: item[6],
              RFID: item[7],
              Status: item[8],
              Keterangan: item[9]
            };
          });
         
          this.tabs[0].filteredData = mappedRiwayat
          this.tabs[0].sortDesc = false

          const response2 = await axios.get('http://192.168.34.201:8099/get_riwayat_gagal'); // Ganti '/api/endpoint' dengan URL API yang sesuai
          const list1 = response2.data
          const mappedRiwayatAkses = list1.map((item) => ({
            BuktiAkses1: item[1],
            WaktuAkses1: moment(item[0]).tz('Asia/Jakarta').format('YYYY-MM-DD HH:mm:ss'),
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
          return this.filteredData;
        } else if (index === 1) {
          return this.filteredDataWaktuAkses;
        }
        return [];
      },
    },

    computed: {
      filteredData() {
        const filteredByStatus = this.filteredDataStatusRiwayat;
        const filteredByTime = this.filteredDataWaktuMasuk;
        return filteredByStatus.filter(item => filteredByTime.includes(item));
      },

      filteredDataStatusRiwayat() {
        if (!this.tabs[0].selectedFilter) {
          return this.tabs[0].filteredData;
        }
        var searchKeyword = parseInt(this.tabs[0].selectedFilter);
        switch (this.tabs[0].selectedFilter) {
          case 'Masih Didalam':
            searchKeyword = 0;
            break;
          case 'Telah Keluar':
            searchKeyword = 1;
            break;
          case 'Bermasalah':
            searchKeyword = 2;
            break;
          default:
            return this.tabs[0].filteredData;
        }
        return this.tabs[0].filteredData.filter(item => {
          const status = item.Status;
          return status === searchKeyword;
        });
      },

      filteredDataWaktuMasuk() {
        if (!this.tabs[0].selectedTimeFilter) {
          return this.tabs[0].filteredData;
        }
        var search = this.tabs[0].selectedTimeFilter.toLowerCase();
        var today = moment().format('YYYY-MM-DD');
        var yesterday = moment().subtract(1, 'day').format('YYYY-MM-DD');
        switch (this.tabs[0].selectedTimeFilter) {
          case 'Hari ini':
            search = today;
            break;
          case 'Kemarin':
            search = yesterday;
            break;
          default:
            return this.tabs[0].filteredData;
        }
        return this.tabs[0].filteredData.filter(item => {
          const date = item.WaktuMasuk.split(' ')[0];
          return date === search;
        });
      },

    filteredDataWaktuAkses() {
      if (!this.tabs[1].selectedTimeFilter) {
          return this.tabs[1].data;
        }
        var search = this.tabs[1].selectedTimeFilter.toLowerCase();
        var today = moment().format('YYYY-MM-DD');
        var yesterday = moment().subtract(1, 'day').format('YYYY-MM-DD');
        switch(this.tabs[1].selectedTimeFilter){
          case("Hari ini"):
            search = today;
            break;
          case 'Kemarin':
            search = yesterday;
            break; 
          default:
            return this.tabs[1].data;
        }
        
        return this.tabs[1].data.filter(item => {
          const date = item.WaktuAkses1.split(' ')[0]
          console.log(date)
            return date === search;
        });
     },
  }
}
</script>

<style scoped>
.title{
color: #FB9503;
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