var express = require("express");
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.use('/static', express.static(__dirname + '/static'));

app.get('/', function(req, res){
  res.sendfile('index.html');
});

app.get('/simple', function(req, res){
  res.sendfile('simple_demo.html');
});

io.on('connection', function(socket){
  console.log('a user connected');
});

http.listen(8000, function(){
  console.log('website serverlistening on *:8000');
});
