const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig ({
  devServer: {
    //proxy: 'https://gpujtk.polban.studio',
    // allowedHosts:'all',
    // host: '0.0.0.0',
    // port: 8090
  },
  transpileDependencies: [
    'vuetify'
  ]
})


