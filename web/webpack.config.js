const path = require('path');
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
  entry: {
  	index: './web/static/js/index.js'
  },
  output: {
    filename: '[name].min.js',
    path: path.resolve(__dirname, './web/static/src')
  },
  plugins: [
    new CleanWebpackPlugin(['./web/static/src']),
    ],
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /\.(png|svg|jpg|gif)$/,
        use: [{
                loader:'url-loader',
                options:{
                    limit:8192,
                    name: '../../static/src/img-webpack/[hash:8].[name].[ext]'
                }
            }]
      },
      // {
      //   test: /\.(woff|woff2|eot|ttf|otf)$/,
      //   use: [
      //     'file-loader'
      //   ]
      // },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        use: [{
                loader:'url-loader',
                options:{
                    name: '../../static/src/font/[name].[ext]'
                }
            }]
      },
      // {
      //   test:/\.(htm|html)$/i,
      //   use:['html-withimg-loader']
        // }
    ],
  }
};