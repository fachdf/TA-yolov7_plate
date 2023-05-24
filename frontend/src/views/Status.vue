<template>
    <v-container class="grey lighten-5">
    <v-row>
      <v-col
      >
        <v-card
          class="left-side"
          outlined
          tile
        >
        <v-row
        class="mb-6"
        no-gutters
        >
        <v-card-title class="title">Status Pengguna Gedung Parkir Polteknik Negeri Bandung</v-card-title>
        </v-row>
        <v-data-table
        :headers="headers"
        :items="contents"
        item-key="name"
        class="elevation-1 pl-4 pr-4"
        >
          <!-- <template v-slot:top>
            <v-switch
            v-model="singleSelect"
            label="Single select"
            class="pa-3"
            ></v-switch>
          </template> -->
          <template v-slot:[`item.Status`]="{ item }">
            <v-chip :color="getStatusColor(item.Status)" dark>
              {{ item.Status }}
            </v-chip>
          </template>
        </v-data-table>
        </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>

  <script>
  export default {
    name: 'riwayat-page',
    data () {
        return {
          headers: [
            {
              text: 'Nama',
              align: 'start',
              sortable: false,
              value: 'Nama',
            },
            { text: 'Status', value: 'Status' },
          ],
          contents: [
            {
              Nama: 'Gate Keluar',
              Status: 'Aktif',
            },
          ],
        }
      },
      methods: {
        getStatusColor(status) {
          // Fungsi ini mengembalikan warna berdasarkan nilai status
          // Sesuaikan dengan logika warna Anda
          if (status === 'Aktif') {
            return 'green';
          } else {
            return 'red';
          }
        }
      }
  };
  </script>
  
  <style scoped>
  .title{
  color: orange;
  font-display: bold;
  font-size: smaller;
  }
  .left-side{
  text-align: right;

  }
  .right-side{
  }
  </style>