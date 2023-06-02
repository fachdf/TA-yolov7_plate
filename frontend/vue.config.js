const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig ({
  devServer: {
    // proxy: 'http://localhost:8099',
    // allowedHosts:'all',
    // host: '0.0.0.0',
    // port: 8090
  },
  transpileDependencies: [
    'vuetify'
  ]
})


