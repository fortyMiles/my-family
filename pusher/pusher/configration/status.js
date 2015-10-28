/*
 *
 * Configuration of conversation events.
 *
 * Author: Minchiuan Gao<minchiuan.gao@gmail.com>
 * Date: 2015-Oct-23
 *
 */

function Events(){
	/*
	 * Define connection events.
	 */
	this.CONNECTION = 'connection';
	// login page
	this.DISCONNECT = 'disconnect';
	// 不管，掉线
	this.LOGOUT = 'logout';
	// log out page
	this.CHAT_MESSAGE = 'chat message';
	// chat page
	this.INVITATION = 'invitation';
	// invitation page
	this.ADD_USER = 'add user';
	this.INFORMATION_RECEIVED = 'information received';
	// chat page
	this.INVITATION_ACCEPT = 'invitation accpet';
	// notification page
	this.ERROR = 'error';
	this.LOGIN = 'login';
	// login page
	this.SENT_TO_RECEIVER = 'sent to receiver';
	// 
	this.SENT_TO_SERVER = 'send to server';
	this.RECEIVER_HAS_READ = 'receiver has read';
	this.FORBIDDEN = 'forbidden';
	this.ALL = 'ALL';

	this.NEW_FRIEND = 'new friend';

	this.test = function(){
		console.log('test');
	};
}

module.exports = Events


