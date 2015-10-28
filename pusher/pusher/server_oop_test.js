/*
 * Change server to oop, test its correctness
 * Author: Minchiuan Gao <minchiuan.gao@gmail.com>
 * Date: 2015-Oct-23
 * 
 * !! Notice: This version, every socket is not define by connected directly, 
 * but search from a login user list. This way could ensure to filter unlogined user
 * to send message, but could make system slow down.
 */

function MainServer(port){

	var io = require('socket.io'),
		events = new require('./configration/status.js');

	var e = new events(),
		User = require('./utility/user_handler.js');

	var Message = require('./configration/message.js'),
		m = new Message();

	this.io_server = io.listen(port);
	this.socket = null;

	this.test = function(){
		console.info('test');
	};

	this.handle_captcha = function(msg){

	};

	this.handle_chat = function(msg){
};

	this.send_message = function(sender, receiver, msg, send_event, feedback_events){
		/* sends a message from sender to receiver.
		 * 
		 * args:
		 *	sender: sender's account name
		 *	receiver: receiver's account name
		 *	message: message content
		 *	send_event: which events neeed send to receiver, such as 'chat message', 'invitation', etc
		 *	feedback_events: which events when send success give back to sender.
		 *
		 */

		if(User.is_login(sender) && User.is_login(receiver)){
				var destination_socket = User.get_socket_by_name(receiver);
				destination_socket.emit(send_event, msg); // router the message to the receiver;
				var sender_socket = User.get_socket_by_name(sender);
				sender_socket.emit(feedback_events, m.SEND_TO_RECEIER);
		}else{
			if(!User.is_login(sender)){
				console.log('user not login');
			}
			// add message to a receiver's unread message.
			if(!User.is_login(receiver)){
				User.add_one_unread_message(receiver, send_event, msg);
			}
		}
	};

	this.handle_invitation = function(msg){
		// invite one person to one's home;
		// after invite, this person could see all the family member of invitor.
		
	};

	this.handle_accpet_invitation = function(msg){
		msg = JSON.parse(msg);
		var sender = msg.sender.trim();
		var receiver = msg.receiver.trim();
		var relation = msg.relation.trim();

		msg = null; // set msg to null, because the add new friend event don't need other message, except sender and receiver.

		User.update_relation(sender, receier, relation);
		this.send_message(sender, receiver, msg, e.NEW_FRIENDS, e.SEND_TO_RECEIVER);
	}

	this.handle_logout = function(msg){
		var user_name = JSON.parse(msg).name;
		User.logout(user_name);
	};

	this.handle_disconnect = function(msg){
		User.disconnect(this.socket);
	};

	this.events_handler = function(socket){
		/*
		 * To maniputlate socket's differect events.
		 */
		console.info('a new client connects you, ( id == ' + socket.id + ' )');

		this.socket = socket;

		this.socket.on(e.LOGIN, function(msg){
			/*
			 * to handle login events.
			 * To notice a user had logined.
			 * ---- 
			 * args:
			 *	 msg: {'name': varchar()};
			 *	 the message that server send.
			 */
			console.log('invitation message');
			console.log(msg);
			//msg = JSON.parse(msg);
			var user_name = msg.name.trim();
			console.info(msg);

			user = new User(user_name, socket, socket.id);
			user.login();

                        var send_message = {message: 'hello ' + user_name};
                        socket.emit(e.CHAT_MESSAGE, send_message);

			if(user.have_unread_message()){
				var unread_messages = user.get_unread_message();

				for(var index = 0; index < unread_messages.length; index++){
					this.socket.emit(unread_messages[index].events, unread_messages[index].message);
				}

				/* !!! notice, need to add a receive confire from client, it's just test code */
				user.delete_unread_message();
			}
		});


		this.socket.on(e.CHAT_MESSAGE, function(msg){
			/*
			 * To handle chat events.
			 * Router each message to its desitination.
			 */

			msg = JSON.parse(msg);
			var sender = msg.sender.trim();
			var receiver = msg.receiver.trim();

			// check if is group chatting. 
			// this version without group chatting function.

			//server.send_message(sender, receiver, msg, e.CHAT_MESSAGE, e.SEND_TO_RECEIVER);

			/* sends a message from sender to receiver.
			 * 
			 * args:
			 *	sender: sender's account name
			 *	receiver: receiver's account name
			 *	message: message content
			 *	send_event: which events neeed send to receiver, such as 'chat message', 'invitation', etc
			 *	feedback_events: which events when send success give back to sender.
			 *
			 */

			if(User.is_login(sender) && User.is_login(receiver)){
					var destination_socket = User.get_socket_by_name(receiver);
					destination_socket.emit(e.CHAT_MESSAGE, msg); // router the message to the receiver;
					var sender_socket = User.get_socket_by_name(sender);
					sender_socket.emit(e.SENT_TO_RECEIVER, m.SEND_TO_RECEIER);
			}else{
				if(!User.is_login(sender)){
					console.log('user not login');
				}
				// add message to a receiver's unread message.
				if(!User.is_login(receiver)){
					User.add_one_unread_message(receiver, e.CHAT_MESSAGE, msg);
				}
			}
		});

		this.socket.on(e.INVITATION, function(msg){
			msg = JSON.parse(msg);
			console.log(msg);
			var sender = msg.sender.trim();
			var receiver = msg.receiver.trim();

			if(User.is_registerred(receiver)){
				if(User.is_login(sender) && User.is_login(receiver)){
					var destination_socket = User.get_socket_by_name(receiver);
					destination_socket.emit(e. INTIVATION, msg); // router the message to the receiver;
					var sender_socket = User.get_socket_by_name(sender);
					sender_socket.emit(e.SENT_TO_RECEIVER, m.SEND_TO_RECEIER);
				}else{
					if(!User.is_login(sender)){
						console.log('user not login');
					}
				// add message to a receiver's unread message.
					if(!User.is_login(receiver)){
						User.add_one_unread_message(receiver, e.CHAT_MESSAGE, msg);
					}
				}
			}else{
				User.send_invitation_phone_text(receiver, function(){
					var sender_socket = User.get_socket_by_name(sender);
					sender_socke.emit(e.SEND_TO_RECEIVER, m.SEND_TO_RECEIER);
				});
			}
		});
		/*
		this.socket.on(e.INVITATION_ACCEPT, this. handle_accpet_invitation);
		this.socket.on(e.LOGOUT, this. handle_logout);
		this.socket.on(e.DISCONNECT, this. handle_disconnect);
		*/
	};

	this.run = function(){
		/* 
		 * run a new process to handle connection.
		 */
		console.info('server start');
		this.io_server.on(e.CONNECTION, this.events_handler);
	};

}

var server = new MainServer(3000);
server.test();
server.send_message();
server.run();
