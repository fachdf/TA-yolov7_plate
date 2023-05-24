<template>
    <v-snackbar v-model="showSnackbar" :color="snackbarColor" :timeout="timeout">
      {{ snackbarText }}
    </v-snackbar>
  </template>
  
  <script>
  export default {
    data() {
      return {
        showSnackbar: false,
        snackbarText: '',
        snackbarColor: '',
        timeout: 3000 // Waktu tampilan notifikasi dalam milidetik
      };
    },
    methods: {
      showNotification(message, color) {
        this.snackbarText = message;
        this.snackbarColor = color;
        this.showSnackbar = true;
      }
    }
  };
  </script>