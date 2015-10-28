// test js OOP
//

function User(){
	this.name = 'name';
	this.age = '18';
	var port = '7777';
	var host = '127.0.0.1';
	var redis = require('redis');
	var clients = redis.createClient(port, host);

	this.test_connect = function(){
		console.info('start to test');
		clients.get('test', function(err, res){
			if(err){
				throw err;
			}else{
				console.info('test okay');
				console.info('end test');
			}
		});
	};

	this.add_a_user = function(user){
		console.log('set a user');
		clients.set('name', 'Gao', redis.print)
	};

	this.get_a_user = function(){
		console.log('get a user');
		return clients.get('name');
	};

	this.set_name = function(new_name){
		this.name = new_name;
	};

	this.say_hello = function(say){
		console.info(say);
	};
}


user = new User();
data = {'name':'Gao', 'age':19};
user.test_connect();
user.add_a_user(data);
console.info('get test');
console.info(user.get_a_user('test'));
/*
user.set_name('new');
user.add_a_user(data);
console.info(user.name);
user.say_hello('hello');
user.get_a_user('Gao');
*/
