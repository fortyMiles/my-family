console.log('import send_message.js success');
var socket = io('http://localhost:3000');
socket.emit('chat message', 'begin');
$('form').submit(function(){
	var message = $('#message').val();

	console.log('message == ' + message);
	socket.emit('chat message', message);
	$('#message').val('');
	return false;
});

socket.on('chat message', function(msg){
	msg = JSON.parse(msg);
	$('#messages').append($('<li>').text(msg.message));
});
socket.on('add user', function(msg){
	$('#users').append($('<li>').text('exised user : ' + msg));
});

