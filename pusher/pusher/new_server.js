/*
 * Nodejs Server saves user information to Redis, it an update edition of old "server.js'
 * Author: Minchiuan Gao <minchiuan.gao@gmail.com>
 * Date: 2015-Oct-21
 */

var io = require('socket.io'),
	io_server = io.listen(3000),
	message = {'sender':null, 'receiver':null, 'message':null, 'status':null},

	user = {'name':null, 'socket':null, 'socket_id':null},
	user_list = [];
	
// declare the server information.
// 

var redis = require('redis'),
	client = redis.createClient();


var CONNECTION = 'connection',
	DISCONNECT = 'disconnect',
	CHAT_MESSAGE = 'chat message',
	ADD_USER = 'add user',
	INFORMATION_RECEIVED = 'information received',
	ERROR = 'error';

function listen_message(socket){
	console.info("New client added in (id = " + socket.id + ").");

	socket.on(CHAT_MESSAGE, function(msg){
		console.log('message == ' + msg);
		msg = JSON.parse(msg);
		sender = msg['sender'].trim();
		receiver = msg['receiver'].trim();
		socket.emit(CHAT_MESSAGE, {'message':'send success'});
		if(sender != 'none'){
			var socket_id = socket.id;
			var socket_json = JSON.stringify(socket);
			user.name = sender;
			user.socket = socket_json;
			user.socket_id = socket_id;
			var user_json = JSON.stringify(user);
			client.set(user.name, user_json, redis.print);
			client.set(user.socket_id, user.name, redis.print);
		}

		if(receiver != 'none'){
			if(receiver == 'all'){
				socket.broadcast.emit(CHAT_MESSAGE, msg);
			}else{
				client.get(user_name, function(error, user){
					if(error != null){
						console.log("error : " + error);
						socket.emit(ERROR, {'message':'no this user'});
					}else{
						var user_info = JSON.parse(user);
						var receiver = user_info.socket;
						receiver.emit(CHAT_MESSAGE,msg);
						socket.emit(CHAT_MESSAGE, {'message':'message received'});
					}
				});
			}
		}
	});

	socket.on(DISCONNECT, function(){
		client.get(socket.id, function(err, user_name){
			if(err != null){
				console.info("Error : " + err);
			}else{
				var name = user_name;
				client.del(name);
				console.info("delete use from redis");
			}
		});
	});
}

io_server.on(CONNECTION, listen_message);
