<template>
    <v-navigation-drawer
      app
      permanent
      left
      width="auto"
    >
      <template v-slot:prepend>
        <v-list-item two-line>
          <v-list-item-avatar>
            <img src="../assets/polban.png">
          </v-list-item-avatar>

          <div class="title">
          <v-list-item-content>
            <v-list-item-title class="text-h6">Sistem Parkir</v-list-item-title>
          </v-list-item-content>
          </div>
        </v-list-item>
        
      </template>

      <v-divider></v-divider>

      <v-list 
      dense
      nav
      >
        <v-list-item
          :to="item.route"
          v-for="item in items"
          :key="item.title"
          link
        >
          <v-list-item-icon>
            <v-icon color="#FB9503">{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

</template>

<script>
  export default {
    name:'Side-bar',
    data () {
      return {
        items: [
          { title: 'Home', icon: 'mdi-home-city', route:'/' },
          { title: 'Riwayat', icon: 'mdi-history', route:'/riwayat' },
          //{ title: 'Riwayat Baru', icon: 'mdi-list-status',route:'/status' },
        ],
        right:null,
      }
    },
  }
</script>

<style>
.title{
  font-size: large;
  color: #FB9503;
}
.icon{
  color: #FB9503;
}
</style>