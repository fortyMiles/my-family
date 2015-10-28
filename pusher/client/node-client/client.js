var
    io = require('socket.io-client'),
    ioClient = io.connect('http://localhost:8000'),
	client_information = {name: '18857453090', message:'test connection'};

function print_message(msg){
	console.info(msg);
}
ioClient.on('foo', print_message);
ioClient.on('received',function(msg){
	console.info('received from server: ' + msg);
});

ioClient.emit('chat message', client_information);

