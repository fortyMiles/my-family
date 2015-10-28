var io = require('socket.io'),
	ioServer = io.listen(3000);

var controller_handler = require('./utility/controller_handler.js');
var user_handler = require('./utility/user_handler.js');
var events = new require('./configration/status.js');
var e = new events();

console.log(e.CONNECTION);
var user = new user_handler();
user.test();

ioServer.on(e.CONNECTION, function(socket) {
	console.info('New client connected (id=' + socket.id + ').');

	socket.on(LOGIN, function(msg){
		/*
		 * args: msg = {'name':varchar}
		 */
		console.info('a new user login');
		msg = JSON.parse(msg);
		user_name = msg.name.trim();

		user.add_a_login_user(username=user_name, socket=socket, user_socket_id=socket_id, function(){
			addUserMessage = {'newUser':user_name};
			ioServer.emit(ADD_USER, user_name);
			// after added, broadcast to every that added a new user;
		});
	});

	socket.on(CHAT_MESSAGE, function(msg){
		console.info(msg);
		msg = JSON.parse(msg);
		sender = msg.sender.trim();
		receiver = msg.receiver.trim();
		message = msg.message;

		socket.emit(SENT_TO_SERVER,'');
		
		// test code
		console.log('send message to sender');
		console.log(sender + ' send message' + 'and he said ' + message);

		if(sender && receiver){
			if(receiver == 'all'){
				socket.broadcast.emit(CHAT_MESSAGE, msg);// don's send to self
			}else{
				if(user.is_login(receiver)){
					var receiver_socket = user.get_socket_by_user(receiver);
					receiver_socket.emit(CHAT_MESSAGE, msg);

					socket.emit(SENT_TO_RECEIVER, '');// send to client, his message it sent to receiver successfully.
				}else{
					var unread_message = {sender:null, message:null, date:null};
					unread_message.receiver = sender;
					unread_message.message = message;
					unread_message.date = new Date();

					user.add_to_unread_list(receiver, unread_message);
				}
			}
		}
	};

	socket.on(INVITATION, function(){
		// invitaion one person.
	});


	socket.on(DISCONNECT, function() {
		var user_index = get_user_by_socket(socket);
		clients.splice(user_index, 1);
		console.info('Client gone (id=' + socket.id + ').');
	});

});

function get_person(user_name){
	var socket = null;
	console.info("point 1" + user_name);
	for(var i = clients.length - 1; i >= 0; i--){
		console.log('clinet name is ' + clients[i].name);
		console.info('clinet. ' + i + ' name == ' + clients[i].name + '  receiver name is ' + user_name);
		if(clients[i].name == user_name){
			socket = clients[i].socket;
			console.info("find a reveiver: " + socket.id);
			break;
		}
	}
	return socket;
}


function get_user_by_socket(socket){
	// based on the socket, and give the index of use in clients list.
	var user_index = null;
	for(var i = 0; i < clients.length; i++){
		if(clients[i].socket_id = socket.id){
			user_index = i;
			console.log('find the user in list');
			break;
		}
	}
	return user_index;
}
