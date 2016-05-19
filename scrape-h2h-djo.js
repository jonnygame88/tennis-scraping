// scrape-career-federer.js

var webPage = require('webpage');
var page = webPage.create();

var fs = require('fs');
var path = 'h2h-djo.html'

page.open('http://www.tennisabstract.com/cgi-bin/player.cgi?p=NovakDjokovic&f=ACareerqqs00&view=h2h', 
function (status) {
  var content = page.content;
  fs.write(path,content,'w')
  phantom.exit();
});