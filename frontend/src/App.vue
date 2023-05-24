<template>
  <v-app>
    <v-main>
      <Sidebar />
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
import Sidebar from '../src/components/Sidebar.vue'
export default {
  name: 'App',
  components: {
      Sidebar,
    },
  data: () => ({
    //
  }),
};
</script>
