var test_value = null;

var user = {"name":"Jhone", "age":19};

function get_value(error, value){
	if(error!=null){
		console.log("error: " + error);
	}else{
		value = JSON.parse(value);
		console.log(value.name);
	}
};

var redis = require("redis"),
	client = redis.createClient();

client.on("error", function(err){
	console.log("Error: " + err);
});


var value = null;


client.set("user", JSON.stringify(user), function(err, res){
	if(err){
		console.log("Error : " + err);
	}
	console.log('set finished');
});

client.get("user", get_value);
client.quit();


