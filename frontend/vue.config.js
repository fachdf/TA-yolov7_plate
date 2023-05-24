const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig ({
  devServer: {
    proxy: 'http://192.168.34.201:8099',
    allowedHosts:'all',
    host: '0.0.0.0',
    port: 8090
  },
  transpileDependencies: [
    'vuetify'
  ]
})


