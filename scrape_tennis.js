// scrape_tennis.js

var webPage = require('webpage');
var page = webPage.create();

var fs = require('fs');
var path = 'tennis.html'

page.open('http://www.tennisabstract.com/cgi-bin/player.cgi?p=RogerFederer&f=ACareerqq', 
function (status) {
  var content = page.content;
  fs.write(path,content,'w')
  phantom.exit();
});