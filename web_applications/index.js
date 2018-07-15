/*
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
     Na Chang (858604)
     Zepeng Dan (933678)
     Junhan Liu (878637)
     Peishan Li (905508)
*/
var express = require('express');
var app = express();
var url = require('url');
var path = require('path');
var nano = require('nano')('http://115.146.86.201:5984');

var bodyParser = require('body-parser');
var fs = require("fs");

var melbourne_obj = JSON.parse(fs.readFileSync(path.join(__dirname,'/data/timeTwi.json')));
var tracking_obj = JSON.parse(fs.readFileSync(path.join(__dirname,'/data/tracking_0503.json')));
var cityList_obj = JSON.parse(fs.readFileSync(path.join(__dirname,'/data/cityList1.json')));
var cityDetail_obj = JSON.parse(fs.readFileSync(path.join(__dirname,'/data/cityDetail1.json')));

var db_name = 'stream_coord';
var stream = nano.db.use(db_name);
app.use(bodyParser.json());
app.use(express.json());

var data = fs.readFileSync(path.join(__dirname,'/data/userTopic10.txt'));
  var topicdata = data.toString();
  var line = topicdata.split('\n');
  for(var i=0 ; i<line.length; i++){
  	var lineElem = line[i].split('	');
  	var topicList = [];
  	var topicNum = [];
  	var userId = lineElem[0].toString();
  	for(j = 1; j<lineElem.length; j++){
  		if(j%2 != 0)
  			topicList.push(lineElem[j]);
  		else
  			topicNum.push(lineElem[j]);
  	}
  	var knum;
  	
  	if(topicList.length > 20)
  		knum = 7;
  	else if(topicList.length > 10)
  		knum = 5;
  	else
  		knum = 3;
  	var randomIndex = [];
  	for(var t=0; t<topicList.length; t++)
  		randomIndex.push(t);
  	var indexList = kRandomArr(randomIndex,knum);
  	if(userId in tracking_obj){
  		tracking_obj[userId].like = [];
  	for(var t_i =0; t_i < knum; t_i++){
  		var temp = {
  			topic:topicList[indexList[t_i]],
  			tweetcount:topicNum[indexList[t_i]]
  		};
  		tracking_obj[userId].like.push(temp);
  	}
  	}
  	else
  		console.log(userId);
  	

  }

app.use(express.static(__dirname));

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});

app.get('/sentiment_result/json/melbourne',function(req,res){
	res.json(melbourne_obj);
});

app.get('/sentiment_result/json/stalking',function(req,res){
	var usernameList = [];
	Object.keys(tracking_obj).forEach(function(key){
		tracking_obj[key].name = tracking_obj[key].name.replace(/\s+/g,"");
		var username = tracking_obj[key].name;
		usernameList.push(username);
	});
	
	res.json(usernameList);
});

app.get('/sentiment_result/json/stalking/:username',function(req,res){
	var userInfo={};
	var username = req.params.username;
	var userList = Object.keys(tracking_obj);
	for(var i=0; i< userList.length;i++){
		var u_id = userList[i];
		var u_name = tracking_obj[u_id].name;
		if(u_name == username){
			userInfo = tracking_obj[u_id];
			break;
		}
	}
	res.json(userInfo);
});

app.get('/sentiment_result/json/city',function(req,res){
	res.json(cityList_obj);

});

app.get('/sentiment_result/json/city/:cityName',function(req,res){
	var cityname = req.params.cityName;
	var cityDetail = cityDetail_obj[cityname];
	res.json(cityDetail);

});

app.get('/streams',function(req,res){
	nano.db.changes('stream_coord', function(err, body) {
  	if (!err) {
    var lat;
    var lng;
    var text;
    var results = body.results;
    //console.log(results);
    var id_list = [];
    for(var i=results.length-100; i<results.length; i++){
    	var id = results[i].id;
    	//console.log(id);
    	id_list.push(id);
    	
    }
    stream.view('StreamDoc','StreamView',{keys:id_list},function(err,body){
    	if (!err) {
    	var sendData = [];
    	body.rows.forEach(function(doc) {
      	//console.log(doc.value);
      	var coord = doc.value[1].coordinates;
      	text = doc.value[0];
    	lat = parseFloat(coord[1]);
    	lng = parseFloat(coord[0]);
    	var temp = {
    		text:text,
    		lat:lat,
    		lng:lng
    	};
    	//console.log(temp);
    	sendData.push(temp);

    });
    	//console.log('sendData',sendData);
    	var num = results.length;
    	var send = {
    		num:num,
    		data:sendData
    	};
    	res.json(send);
  	}
    });
 
  }
});
});

app.post('/streams/change',function(req,res){
	var request = req.body;
	var pre_index = request.pre_index;
	nano.db.changes('stream_coord', function(err, body) {
  	if (!err) {
    var lat;
    var lng;
    var text;
    var results = body.results;
    //console.log(results);
    var id_list = [];
    for(var i=pre_index ; i<results.length; i++){
    	var id = results[i].id;
    	//console.log(id);
    	id_list.push(id);
    	
    }
    stream.view('StreamDoc','StreamView',{keys:id_list},function(err,body){
    	if (!err) {
    	var sendData = [];
    	body.rows.forEach(function(doc) {
      	//console.log(doc.value);
      	var coord = doc.value[1].coordinates;
      	text = doc.value[0];
    	lat = parseFloat(coord[1]);
    	lng = parseFloat(coord[0]);
    	var temp = {
    		text:text,
    		lat:lat,
    		lng:lng
    	};
    	//console.log(temp);
    	sendData.push(temp);

    });
    	//console.log('sendData',sendData);
    	res.json(sendData);
  	}
    });
 
  }
});
});



function kRandomArr( arr, length ){
    var newArr = [];
    var index;

    for(var i = 0 ; i < length; i++ ){

        index = parseInt( Math.random() * arr.length );
        newArr.push( arr[index] );
        arr.splice( index, 1 );
    }

    return newArr;
};