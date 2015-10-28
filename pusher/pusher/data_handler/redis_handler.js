/*
 * Handle CRUD opeartion in redis.
 * Author: Minchuian Gao<mqgao@outlook.com>
 * Date: 2015-Oct-21
 */


function RedisHandler(){
	var redis = require('redis');

	var client = redis.createClient();
	this.user_id = 0;

	this.create_a_user = function(user){
		this.client.hset(user.user_name, user);
	};

	this.give_a_user = function(user_name){
		// return a user's information by its name.
		if(this.client.hexists(user_name)){
			return this.client.hget(user.user_name);
		}else{
			return false;
		}
	};

	this.delete_a_user = function(user_name){
		return this.client.hdel(user_name);
	};
	*/
}

user = {'user_name':'Gao', 'age':22};

redisHandler = RedisHandler();
/*
redisHandler.create_a_user(user);
console.info(redisHandler. give_a_user('Gao'));
redisHandler.delete_a_user('Gao');
console.info(redisHandler. give_a_user('Gao'));
*/
