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
var overlaySet = [];
var crowd = {
		"1": [
			[-37.814,144.96332],
			[-37.824,144.96332]
		],
		"2": [
			[-37.924,144.962],
			[-37.824,144.96332]
		],
		"3": [
			[-37.98,144.82],
			[-37.14,144.26332]
		],
		"4": [
			[-37.98,144.82],
			[-37.14,144.22]
		]
	};

var timeSet = [["0","1","2","3"],["4","5","6","7"],["8","9","10","11"],["12","13","14","15"],["16","17","18","19"],["20","21","22","23"]];
   

function transformCrowdData(data){
	var t_data = [];
	Object.keys(data).forEach(function(key){
		var newlist = data[key];
		for(var i=0; i<newlist.length; i++){
			var lat = parseFloat(newlist[i][0]);
			var lng = parseFloat(newlist[i][1]);
			var time = key;
			var tempdata ={
				Lat:lat,
				Lng:lng,
				time:time
			};
			t_data.push(tempdata);
		}
	});
	return t_data;
}

function d3show(crowd_data){
    deleteOverlay();
    var overlay = new google.maps.OverlayView();
    overlaySet.push(overlay);
    overlay.onAdd = function(){
        var layer = d3.select(this.getPanes().overlayMouseTarget)
                .append("div")
                .attr("class","tweet");
        overlay.draw = function(){
                var projection = this.getProjection(),
                    padding = 8;

                var marker = layer.selectAll("svg")
                    .data(crowd_data)
                    .each(transform)
                    .enter()
                    .append("svg")
                    .each(transform);

                var r =4;
                

                marker.append("circle")
                    .attr("cx",padding)
                    .attr("cy",padding)
                    .attr("r",r)
                    .attr("stroke",function(d){
                        if(timeSet[0].indexOf(d.time) >= 0)
                            return colores_google(1);
                        else if(timeSet[1].indexOf(d.time) >= 0)
                            return colores_google(2);
                        else if(timeSet[2].indexOf(d.time) >= 0)
                            return colores_google(3);
                        else if(timeSet[3].indexOf(d.time) >= 0)
                            return colores_google(4);
                        else if(timeSet[4].indexOf(d.time) >= 0)
                            return colores_google(5);
                        else 
                            return colores_google(6);

                    })
                    .attr("stroke-opacity",0.65)
                    .attr("stroke-width","2px")
                    .attr("fill",function(d){
                        if(timeSet[0].indexOf(d.time) >= 0)
                            return colores_google(1);
                        else if(timeSet[1].indexOf(d.time) >= 0)
                            return colores_google(2);
                        else if(timeSet[2].indexOf(d.time) >= 0)
                            return colores_google(3);
                        else if(timeSet[3].indexOf(d.time) >= 0)
                            return colores_google(4);
                        else if(timeSet[4].indexOf(d.time) >= 0)
                            return colores_google(5);
                        else 
                            return colores_google(6);
                    })
                    .attr("fill-opacity",0.65);
          

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
          d3.selectAll(".tweet")
                    .remove();

        };

     //overlay.setMap(map);
     setOverlay(map);
}

function colores_google(n) {
  var colores_g = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"];
  return colores_g[n % colores_g.length];
}

function setOverlay(map){
  for(var i = 0; i < overlaySet.length; i++){
    overlaySet[i].setMap(map);
  }
}

function deleteOverlay()
{
  setOverlay(null);
  overlaySet = [];
}

var allTweet;
function initMap()
{

    map = new google.maps.Map(document.getElementById('melbourne_map'), {
        zoom: 10,
        center: { lat: -37.814, lng: 144.96332 },
        styles:[
  {
    "featureType": "poi",
    "elementType": "labels.text",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "poi.business",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "labels.icon",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "featureType": "transit",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  }
]

    });
    //var crowd_data =transformCrowdData(crowd);

    var getData = $.ajax({
    url:'/sentiment_result/json/melbourne',
    type: 'GET', 
    contentType:'application/json',
    dataType:'json',
    }).done(function (res) {
    var crowd_data =transformCrowdData(res);
    d3show(crowd_data);
    allTweet = crowd_data;
    
    });

    document.getElementById('time0').addEventListener('click', function() {
        d3ShowTime(0);
    });
    document.getElementById('time1').addEventListener('click', function() {
        d3ShowTime(1);
    });
    document.getElementById('time2').addEventListener('click', function() {
        d3ShowTime(2);
    });
    document.getElementById('time3').addEventListener('click', function() {
        d3ShowTime(3);
    });
    document.getElementById('time4').addEventListener('click', function() {
        d3ShowTime(4);
    });
    document.getElementById('time5').addEventListener('click', function() {
        d3ShowTime(5);
    });

}

function d3ShowTime(index){
    deleteOverlay();
    var overlay = new google.maps.OverlayView();
    overlaySet.push(overlay);
    overlay.onAdd = function(){
        var layer = d3.select(this.getPanes().overlayMouseTarget)
                .append("div")
                .attr("class","tweet");
        overlay.draw = function(){
                var projection = this.getProjection(),
                    padding = 8;

                var marker = layer.selectAll("svg")
                    .data(allTweet)
                    .each(transform)
                    .enter()
                    .append("svg")
                    .each(transform);

                var r =4;
                

                marker.append("circle")
                    .attr("cx",padding)
                    .attr("cy",padding)
                    .attr("r",r)
                    .attr("stroke",function(d){
                        if(timeSet[0].indexOf(d.time) >= 0)
                            return colores_google(1);
                        else if(timeSet[1].indexOf(d.time) >= 0)
                            return colores_google(2);
                        else if(timeSet[2].indexOf(d.time) >= 0)
                            return colores_google(3);
                        else if(timeSet[3].indexOf(d.time) >= 0)
                            return colores_google(4);
                        else if(timeSet[4].indexOf(d.time) >= 0)
                            return colores_google(5);
                        else 
                            return colores_google(6);

                    })
                    .attr("stroke-opacity",function(d){
                        if(timeSet[index].indexOf(d.time) >= 0)
                            return 0.7;
                        else
                            return 0.0;
                    })
                    .attr("stroke-width","2px")
                    .attr("fill",function(d){
                        if(timeSet[0].indexOf(d.time) >= 0)
                            return colores_google(1);
                        else if(timeSet[1].indexOf(d.time) >= 0)
                            return colores_google(2);
                        else if(timeSet[2].indexOf(d.time) >= 0)
                            return colores_google(3);
                        else if(timeSet[3].indexOf(d.time) >= 0)
                            return colores_google(4);
                        else if(timeSet[4].indexOf(d.time) >= 0)
                            return colores_google(5);
                        else 
                            return colores_google(6);
                    })
                    .attr("fill-opacity",function(d){
                        if(timeSet[index].indexOf(d.time) >= 0)
                            return 0.7;
                        else
                            return 0.0;
                    });
          

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
          d3.selectAll(".tweet")
                    .remove();

        };

     //overlay.setMap(map);
     setOverlay(map);

}

