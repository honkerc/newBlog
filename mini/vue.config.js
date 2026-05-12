const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
    transpileDependencies: true,
    publicPath: './',
    devServer: {
        host: '0.0.0.0',
        port: 3001,
        allowedHosts: 'all',
    },
    configureWebpack: {
        context: path.resolve(__dirname),
    },
})
