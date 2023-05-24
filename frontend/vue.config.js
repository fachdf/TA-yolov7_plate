const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig ({
  devServer: {
    proxy: 'https://gpujtk.polban.studio'
  },
  transpileDependencies: [
    'vuetify'
  ]
})


