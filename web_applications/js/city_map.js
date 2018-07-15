/*
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
     Na Chang (858604)
     Zepeng Dan (933678)
     Junhan Liu (878637)
     Peishan Li (905508)
*/
var map;
var chart;
function d3show(city_data){
	 var overlay = new google.maps.OverlayView();
    overlay.onAdd = function(){
        var layer = d3.select(this.getPanes().overlayMouseTarget)
                .append("div")
                .attr("class","city");
        overlay.draw = function(){
                var projection = this.getProjection(),
                    padding = 40;

                var marker = layer.selectAll("svg")
                    .data(city_data)
                    .each(transform)
                    .enter()
                    .append("svg")
                    .each(transform);

                var r =38;

                marker.append("circle")
                    .attr("cx",padding)
                    .attr("cy",padding)
                    .attr("r",r)
                    .attr("stroke","#dc3912")
                    .attr("stroke-opacity",0.7)
                    .attr("stroke-width","2px")
                    .attr("fill","#dc3912")
                    .attr("fill-opacity",0.7)
                    .attr("id",function(i){
                    	return "Marker"+i;
                    })
                    .on("click",function(d,i){
                    	
                        map.setZoom(11);
                        var newCenter ={
                        	lat: d.Lat,
                        	lng: d.Lng
                        }
  						map.setCenter(newCenter);
  						//showStatistic();
  						getCityDetail(d.content.name);
  						
                    });

                    marker.append("text")
                	  .text(function(d){
                	  	return d.content.name;
                	  })
                      .attr("x",10)
                      .attr("y",15)
                      .attr("font-size", 15)
                      .attr("font-family", "simsum");

                	marker.append("text")
                	  .text(function(d){
                	  	return d.content.Pos;
                	  })
                      .attr("x",10)
                      .attr("y",35)
                      .attr("font-size", 15)
                      .attr("font-family", "simsum");

                	marker.append("text")
                	  .text(function(d){
                	  	return d.content.Neg;
                	  })
                      .attr("x",10)
                      .attr("y",55)
                      .attr("font-size", 15)
                      .attr("font-family", "simsum");
                
                

                    function transform(d){
                    d = new google.maps.LatLng(d.Lat,d.Lng);
                    d = projection.fromLatLngToDivPixel(d);
                    return d3.select(this)
                        .style("left",(d.x - padding) + "px")
                        .style("top",(d.y - padding) + "px")
                    }
                };
    };
           
    
    overlay.onRemove = function()
        {
          d3.selectAll(".city")
                    .remove();

        };

     overlay.setMap(map);
}


function initMap()
{
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 5,
        center: { lat: -28.024, lng: 135.887 },
        styles:[
  {
    "featureType": "poi.business",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "labels.text",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  }
]
    });
    $('button').css('display','none');
    $('#selectSuburb').css('display','none');

    var getData = $.ajax({
    url:'/sentiment_result/json/city',
    type: 'GET', 
    contentType:'application/json',
    dataType:'json',
    }).done(function (res) {
    var city_data =res.cityList;
    d3show(city_data);
    
    });

}

function getCityDetail(cityName){
	//console.log("beginCity");
	var url = '/sentiment_result/json/city/'+cityName;
	var getData = $.ajax({
    url:url,
    type: 'GET', 
    contentType:'application/json',
    dataType:'json',
    }).done(function (res) {
    city_details = res;
    showStatistic(city_details);
   // console.log(city_details);
    
    });
}

function showStatistic(city_details){

    var lineData = city_details;
	var options = Object.keys(lineData.cities);
	for(var i=0;i<options.length;i++){
		var option = options[i];
		$("#suburb").append("<option value='"+option+"'>"+option+"</option>");
	}
	$(document).ready(function() {
     $(".chosen-select").chosen({width:"350px"});
  });

  $('.statistic').css({'width':'50%','height':'100%','margin-left':'50%'});
  $('#map').css({'width':'50%','margin-left':'0px'});
  $('button').css('display','block');
  $('#selectSuburb').css('display','block');

}

function initialStatistic(){

var ctx = document.getElementById('myChart').getContext('2d');
var lineData = city_details;
//var x_labels = Object.keys(lineData.suburbs);
var x_labels = $('#suburb').val();
//console.log(x_labels);
var totalTweet = [];
var totalPos = [];
//var percent = [];
var income = [];
var health = [];
//var traffic = [];
Object.keys(lineData.cities).forEach(function(key){

if(x_labels.indexOf(key) >= 0){
	var temp = lineData.cities[key];
 	totalTweet.push(parseFloat(temp.totalTweet));
 	totalPos.push(parseFloat(temp.totalPos));
 	//percent.push(parseFloat(temp.totalPos)/parseFloat(totalTweet));
 	income.push(parseFloat(temp.income));
 	health.push(parseFloat(temp.health));
 	//traffic.push(parseFloat(temp.trafficAccident));
}

});

var temp1 = [];
for(var i = 0; i<totalTweet.length; i++){
	temp1.push(totalTweet[i]);
}
temp1.sort(sortNumber);
var min_tweet = temp1[0];
var max_tweet = temp1[temp1.length-1];
for(var i = 0; i<totalTweet.length; i++){
	totalTweet[i] = 0.2 + 0.8*(totalTweet[i]-min_tweet)/(max_tweet - min_tweet);
}

var temp2 = [];
for(var i = 0; i<totalPos.length; i++){
	temp2.push(totalPos[i]);
}
temp2.sort(sortNumber);
var min_pos = temp2[0];
var max_pos = temp2[temp2.length-1];
for(var i = 0; i<totalPos.length; i++){
	totalPos[i] = 0.2 + 0.8*(totalPos[i]-min_pos)/(max_pos - min_pos);
}
/*
var temp3 = [];
for(var i = 0; i<percent.length; i++){
	temp3.push(percent[i]);
}
temp3.sort(sortNumber);
var min_p = temp3[0];
var max_p = temp3[temp3.length-1];
for(var i = 0; i<percent.length; i++){
	percent[i] = 0.2 + 0.8*(percent[i]-min_p)/(max_p - min_p);
}
*/
var temp4 = [];
for(var i = 0; i<income.length; i++){
	temp4.push(income[i]);
}
temp4.sort(sortNumber);
var min_i = temp4[0];
var max_i = temp4[temp4.length-1];
for(var i = 0; i<income.length; i++){
	income[i] = 0.2 + 0.8*(income[i]-min_i)/(max_i - min_i);
}

var temp5 = [];
for(var i = 0; i<health.length; i++){
	temp5.push(health[i]);
}
temp5.sort(sortNumber);
var min_h = temp5[0];
var max_h = temp5[temp5.length-1];
for(var i = 0; i<health.length; i++){
	health[i] = 0.2 + 0.8*(health[i]-min_h)/(max_h - min_h);
}
/*
var temp6 = [];
for(var i = 0; i<traffic.length; i++){
	temp6.push(traffic[i]);
}
temp6.sort(sortNumber);
var min_tra = temp6[0];
var max_tra = temp6[temp6.length-1];
for(var i = 0; i<traffic.length; i++){
	traffic[i] = 0.2 + 0.8*(traffic[i]-min_tra)/(max_tra - min_tra);
}
*/

var config = {

    type: 'line',

    // dataset
    data: {
        labels:x_labels ,
        datasets: []
    },
    options: {
        elements: {
            line: {
                tension: 0, // disables bezier curves
            }
        }
    }

};
chart = new Chart(ctx, config);

var count1=0;
var count2=0;
var count3=0;
var count4=0;
var count5=0;
var count6=0;

document.getElementById('totalTweet').addEventListener('click', function() {
			count1++;
			if(count1%2 == 1){
				var newDataset = {
				label: "Total Tweets",
            	backgroundColor: colores_google(1),
            	borderColor: colores_google(1),
            	data: totalTweet,
            	fill: false,
			};

			config.data.datasets.push(newDataset);
			chart.update();
			}
			else{
				var len = config.data.datasets.length;
				for(var i=0; i<len;i++){
					if(config.data.datasets[i].label == "total tweets"){
						config.data.datasets.splice(i,1);
						break;
					}
				}
				chart.update();
			}
			
		});

document.getElementById('totalPos').addEventListener('click', function() {
			count2++;
			if(count2%2 == 1){
				var newDataset = {
				label: "Total Positive Tweets",
            backgroundColor: colores_google(2),
            borderColor: colores_google(2),
            data: totalPos,
            fill: false,
			};

			config.data.datasets.push(newDataset);
			chart.update();
			}
			else{
				var len = config.data.datasets.length;
				for(var i=0; i<len;i++){
					if(config.data.datasets[i].label == "total positive tweets"){
						config.data.datasets.splice(i,1);
						break;
					}
				}
				chart.update();
			}
			
		});
/*
document.getElementById('percent').addEventListener('click', function() {
			count3++;
			if(count3%2 == 1){
				var newDataset = {
            label: "positive tweets percentage",
            backgroundColor: colores_google(3),
            borderColor: colores_google(3),
            data: percent,
            fill: false,
        };

			config.data.datasets.push(newDataset);
			chart.update();
			}
			else{
				var len = config.data.datasets.length;
				for(var i=0; i<len;i++){
					if(config.data.datasets[i].label == "positive tweets percentage"){
						config.data.datasets.splice(i,1);
						break;
					}
				}
				chart.update();
			}
			
		});
*/

document.getElementById('income').addEventListener('click', function() {
			count4++;
			if(count4%2 == 1){
				var newDataset = {
            label: "Income",
            backgroundColor: colores_google(4),
            borderColor: colores_google(4),
            data: income,
            fill: false,
        };

			config.data.datasets.push(newDataset);
			chart.update();
			}
			else{
				var len = config.data.datasets.length;
				for(var i=0; i<len;i++){
					if(config.data.datasets[i].label == "income"){
						config.data.datasets.splice(i,1);
						break;
					}
				}
				chart.update();
			}
			
		});

document.getElementById('health').addEventListener('click', function() {
			count5++;
			if(count5%2 == 1){
				var newDataset = {
            label: "Health",
            backgroundColor: colores_google(5),
            borderColor: colores_google(5),
            data: health,
            fill: false,
        };

			config.data.datasets.push(newDataset);
			chart.update();
			}

			else{
				var len = config.data.datasets.length;
				for(var i=0; i<len;i++){
					if(config.data.datasets[i].label == "health"){
						config.data.datasets.splice(i,1);
						break;
					}
				}
				chart.update();
			}

		});

/*
document.getElementById('traffic').addEventListener('click', function() {
			count6++;
			if(count6%2 == 1){
				var newDataset = {
            label: "traffic accident",
            backgroundColor: colores_google(6),
            borderColor: colores_google(6),
            data: traffic,
            fill: false,
        };

			config.data.datasets.push(newDataset);
			chart.update();
			}

			else{
				var len = config.data.datasets.length;
				for(var i=0; i<len;i++){
					if(config.data.datasets[i].label == "traffic accident"){
						config.data.datasets.splice(i,1);
						break;
					}
				}
				chart.update();
			}
		});
		*/
}

function getCityData(){
	$.getJSON("js/cityPage.json",function(data){
	});
}

function sortNumber(a,b)
{
return a - b;
}

function colores_google(n) {
  var colores_g = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"];
  return colores_g[n % colores_g.length];
}
