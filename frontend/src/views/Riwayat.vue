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
        <v-card-text>
        <p class="text-h6 text-color-#FB9503" color="#FB9503"> Keterangan Status</p>
        <p>
          0 = Mahasiswa masih didalam area parkir 
          <br> 
          1 = Mahasiswa sudah keluar area parkir
          <br>
          2 = Mahasiswa masih didalam area parkir (masalah)
        </p>
      </v-card-text>
      <v-row>
        <v-col 
        sm="5"
        md="6"
        mr=auto 
        >
          <v-select
          max-width="344"
          class="left-input pt-4 pl-4 mx-auto"
          v-model="tab.selectedFilter"
          :items="tab.filterOptions"
          label="Filter Status"
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
          <v-select
          max-width="344"
          class="pt-4 pr-4 mx-auto"
          v-model="tab.selectedTimeFilter"
          :items="tab.timeFilterOptions"
          label="Filter Waktu Masuk"
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
        :sort-desc.sync="tab.sortAsc"
        class="elevation-1 pl-4 pr-4">
          <template v-slot:[`item.BuktiMasuk`]="{ item }">
            <v-btn color="primary" rounded @click="openDialog(item.BuktiMasuk)">
              Lihat
            </v-btn>
          </template>
          <template v-slot:[`item.BuktiKeluar`]="{item}">
            <v-btn color="primary" rounded @click="openDialog(item.BuktiKeluar)">
              Lihat
            </v-btn>
          </template>
          <template v-slot:[`item.BuktiAkses`]="{item}">
            <v-btn color="primary" rounded @click="openDialog(item.BuktiKeluar)">
              Lihat
            </v-btn>
          </template>
          <template v-slot:[`item.BuktiAkses1`]="{item}">
            <v-btn color="primary" rounded @click="openDialog(item.BuktiAkses1)">
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
            timeFilterOptions: ['All', 'Today', 'Yesterday'],
            filteredData:[],
            sortBy: 'WaktuMasuk',
            sortAsc: false,
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
            // { text: 'ID Mahasiswa', value: 'IDMahasiswa1' },
            { text: 'Pelat Nomor', value: 'PelatNomor1', sortable: false, },
            { text: 'Waktu Akses', value: 'WaktuAkses1' },
            { text: 'Bukti Akses', value: 'BuktiAkses1', sortable: false, },
            { text: 'Status', value: 'Status1', sortable: false, },
            { text: 'Keterangan', value: 'Keterangan1', sortable: false, },
            ],
            data: [],
            selectedFilter: null,
            filterOptions: ['3'],
            timeFilterOptions: ['All', 'Today', 'Yesterday'],
            filteredData:[],
            sortBy: 'WaktuAkses1',
            sortAsc: false,
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
      //setInterval(this.getDataRiwayat,3000);
    },

    methods: {
      async getDataRiwayat() {
        try {
          const response1 = await axios.get('http://192.168.34.201:8099/get_riwayat_parkir'); // Ganti '/api/endpoint' dengan URL API yang sesuai
          const list = response1.data 
          // const mappedRiwayat = list.map((item) => ({
          //   BuktiKeluar: item[2],
          //   BuktiMasuk: item[0],
          //   PelatNomor: item[4],
          //   RFID: item[5],
          //   Status: item[6],
          //   WaktuKeluar: moment(item[3]).tz('Asia/Jakarta').format('YYYY-MM-DD HH:mm:ss') || "No Data",
          //   WaktuMasuk: moment(item[1]).tz('Asia/Jakarta').format('YYYY-MM-DD HH:mm:ss'),
          //   Keterangan: item[7]
          // }));
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
         
          this.tabs[0].data = mappedRiwayat
          this.tabs[0].filteredData = this.filterDataBySelectedTime(mappedRiwayat);
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
          return this.filteredData1;
        } else if (index === 1) {
          return this.filteredData2;
        }
        return [];
      },

      filterDataByToday(data) {
        const today = new Date().toISOString().split('T')[0]; // Mendapatkan tanggal hari ini dalam format YYYY-MM-DD
        // console.log("data masuk")
        // console.log(this.item.WaktuMasuk.split(' ')[0]);
        return data.filter(item => {
          const date = item.WaktuMasuk.split(' ')[0]; // Mendapatkan tanggal dari kolom WaktuMasuk dalam format YYYY-MM-DD
          console.log("Datamasuk")
          console.log(date)
          console.log(today)
          return date === today; // Filter data berdasarkan hari ini
        });
      },

      filterDataByYesterday(data) {
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(today.getDate() - 1);
        const yesterdayString = yesterday.toISOString().split('T')[0]; // Mendapatkan tanggal kemarin dalam format YYYY-MM-DD
        return data.filter(item => {
          const date = item.WaktuMasuk.split(' ')[0]; // Mendapatkan tanggal dari kolom WaktuMasuk dalam format YYYY-MM-DD
          return date === yesterdayString; // Filter data berdasarkan kemarin
        });
      },
      
      filterDataBySelectedTime(data) {
        if (this.selectedTimeFilter === 'Today') {
          return this.filterDataByToday(data); // Filter data berdasarkan hari ini
        } else if (this.selectedTimeFilter === 'Yesterday') {
          return this.filterDataByYesterday(data); // Filter data berdasarkan kemarin
        } else {
          return data; // Tampilkan semua data jika tidak ada filter waktu yang dipilih
        }
      },
    },

    computed: {
      filteredData1() {
        if (!this.tabs[0].selectedFilter && !this.tabs[0].selectedTimeFilter) {
          return this.tabs[0].filteredData;
        }
        var searchKeyword = parseInt(this.tabs[0].selectedFilter);
        switch(this.tabs[0].selectedFilter){
          case("Masih Didalam"):
            searchKeyword = 0;
            break;
          case("Telah Keluar"):
            searchKeyword = 1;
            break;
          case("Bermasalah"):
            searchKeyword = 2;
            break;
          default:
            return this.tabs[0].filteredData;
        }
        //const searchKeyword = parseInt(this.tabs[0].selectedFilter);
        //console.log(searchKeyword)
        return this.tabs[0].filteredData.filter(item => {
          console.log(this.tabs[0].selectedTimeFilter)
          //const status = item.Status;
           return (searchKeyword == item.Status) && (this.filterDataBySelectedTime(item.WaktuMasuk));
          //return (!searchKeyword || status == searchKeyword);
        });
     },

      filteredData2() {
        if (!this.tabs[1].selectedFilter && !this.tabs[1].selectedTimeFilter) {
          return this.tabs[1].data;
        }

        const searchKeyword = parseInt(this.tabs[1].selectedFilter);

        return this.tabs[1].data.filter(item => {
          const status = item.Status1;
          const date = item.WaktuAkses1.split(' ')[0]

          return (status === searchKeyword || searchKeyword === 0) &&
          (!this.tabs[1].selectedTimeFilter || this.filterDataBySelectedTime(date));
        });
      }
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