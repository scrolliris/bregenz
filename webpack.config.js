'use strict';

var path = require('path')
  , webpack = require('webpack')
  , ExtractTextPlugin = require('extract-text-webpack-plugin')
  , ManifestPlugin = require('webpack-manifest-plugin')
  , LicenseWebpackPlugin = require('license-webpack-plugin')
  ;

var nodeEnv = process.env.NODE_ENV || 'production';
console.log('» webpack:', nodeEnv);

var filename = '[name]';
if (nodeEnv === 'production') {
  filename += '.[contenthash]';
}
var stylusBundler = new ExtractTextPlugin(filename + '.css')
  , svgBundler = new ExtractTextPlugin('img/' + filename + '.svg')
  ;

var appName = 'willisau'
  ;

var config = {
  output: {
    path: path.resolve(__dirname, 'tmp/build/')
  , filename: (nodeEnv === 'production' ?
      '[name].[chunkhash].js' : '[name].js')
  }
, module: {
    loaders: [{ // semantic-ui
      test: /\.css$/
    , loader: stylusBundler.extract(['css'])
    }, {
      test: /\.styl$/
    , loader: stylusBundler.extract(['css', 'stylus'])
    , include: [
        path.resolve(__dirname, appName + '/assets')
      ]
    }, {
      test: /\.js$/
    , loader: 'babel-loader'
    , include: [
        path.resolve(__dirname, appName + '/assets')
      ]
    }, { // open-iconic
      test: /open-iconic\.min\.svg$/
    , loader: svgBundler.extract(['svg-sprite'])
    , include: [
        path.resolve(__dirname,
          'node_modules/open-iconic/sprite/open-iconic.min.svg')
      ]
    }]
  }
, resolve: {
    extensions: ['', '.css', '.js', '.svg']
  , alias: {
      'styr\.css$': 'styr/dst/styr.min.css'
    , 'open-iconic\.svg$': 'open-iconic/sprite/open-iconic.min.svg'
    }
  }
, plugins: (function() {
    var _plugins = [
      stylusBundler
    , svgBundler
    ];
    _plugins.push(
      new webpack.EnvironmentPlugin([
       'NODE_ENV'
      ])
    );
    _plugins.push(
      new webpack.DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify(nodeEnv)
      })
    );
    _plugins.push(
      new webpack.ProvidePlugin({
        'jQuery': 'jquery'
      , 'window.d3': 'd3\.js'
      , 'window.moment': 'moment\.js'
      })
    );
    if (nodeEnv === 'production') {
      _plugins.push(
        new ManifestPlugin({
          fileName: 'manifest.json'
        })
      );
      _plugins.push(
        new LicenseWebpackPlugin({
          pattern: /^(MIT|ISC|BSD.*)$/
        , filename: 'freesoftware-licenses.txt'
        , addLicenseText: false
        , licenseFilenames: [
          // These filese are needed to check license in package.json.
            'LICENSE', 'LICENSE.md', 'LICENSE.txt'
          , 'license', 'license.md', 'license.txt'
          , 'README', 'README.md', 'README.txt'
          , 'readme', 'readme.md', 'readme.txt'
          ]
        })
      );
      _plugins.push(
        new webpack.optimize.UglifyJsPlugin({
          debug: false
        , minimize: true
        , compress: {
            warnings: false
          }
        , output: {
            comments: false
          }
        })
      );
    }
    return _plugins;
  })()
};

module.exports = config;
