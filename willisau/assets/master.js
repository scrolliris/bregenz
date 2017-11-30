// vendor
import 'styr.css'
import 'open-iconic.svg'

// global styles
import './css/typography.styl'
import './css/layout.styl'

// application
import './css/index.styl'


var FontFaceObserver = require('fontfaceobserver.js');
var font = new FontFaceObserver('Roboto Slab');
font.load().then(function() {
  document.body.classList.add('slab-loaded');
})

var font = new FontFaceObserver('Open Sans');
font.load().then(function() {
  document.body.classList.add('sans-loaded');
})
