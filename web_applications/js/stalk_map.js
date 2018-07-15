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
var myBarChart;
function searchUser() {
   //define variables
    var input, filter, ul, li, a, i;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByTagName('li');
 
    // loop to find the matched ones
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

function transformUserData(data){
	var t_data = [];
	Object.keys(data.tracking).forEach(function(key){
		var newlist = data.tracking[key];
		for(var i=0; i<newlist.length; i++){
			var lat = newlist[i][1];
			var lng = newlist[i][0];
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

function getUserInfo(input){
   // console.log(input);
    var search = document.getElementById('myInput');
    search.value = input.toString();
    var url = '/sentiment_result/json/stalking/' + input;
    var getData = $.ajax({
    url: url,
    type: 'GET', 
    contentType:'application/json',
    dataType:'json',
    }).done(function (res) {
    var userInfo = res;
   // console.log(userInfo);
    var userData;
    userData = transformUserData(userInfo);
    
    var Lat = -28.024;
    var Lng = 135.887;
    /*
    for(var i=0; i<userData.length;i++){
        Lat += userData[i].Lat;
        Lng += userData[i].Lng;
    }
    Lat = Lat/userData.length;
    Lng = Lng/userData.length;
    */
    var newCenter ={
        lat: Lat,
        lng: Lng
    }

    map.setCenter(newCenter);
    map.setZoom(5);
    d3Show(userData,userInfo);

    });
}

function d3Show(userData,userInfo){
    var timeSet = [["0","1","2","3"],["4","5","6","7"],["8","9","10","11"],["12","13","14","15"],["16","17","18","19"],["20","21","22","23"]];

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
                    .data(userData)
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
                    .attr("stroke-opacity",0.8)
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
                    .attr("fill-opacity",0.8);
          

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

     setOverlay(map);
     showLike(userInfo);

}

function colores_google(n) {
  var colores_g = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"];
  return colores_g[n % colores_g.length];
}

function showLike(userInfo){
    var topiclist = userInfo.like;
    var y_labels = [];
    var dataset = [];
    var userText = "The topics "+userInfo.name+" likes:"
    for(var i = 0;i<topiclist.length;i++){
        y_labels.push(topiclist[i].topic);
        dataset.push(topiclist[i].tweetcount);
    }

    var bardata ={
        labels:y_labels,
        datasets:[{
            label:'twitter topics',
            backgroundColor: colores_google(6),
            borderColor: colores_google(6),
            borderWidth: 1,
            data:dataset
        }
        ]
    };

    var ctx = document.getElementById('likeChart').getContext('2d');
    myBarChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: bardata,
    options: {
        // Elements options apply to all of the options unless overridden in a dataset
        // In this case, we are setting the border of each horizontal bar to be 2px wide
        elements: {
            rectangle: {
                borderWidth: 2,
                        }
        },
        responsive: true,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        },
        
        title: {
             display: true,
            text: userText
            }
    }
    });
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

function initMap()
{
    map = new google.maps.Map(document.getElementById('stalk_map'),{
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

    var getData = $.ajax({
    url:'/sentiment_result/json/stalking',
    type: 'GET', 
    contentType:'application/json',
    dataType:'json',
    }).done(function (res) {
    var userList =res;
   // console.log(userList);
    initialUserList(userList);

    });
  
}

function initialUserList(user_data){
    var users = user_data;
    users.sort();
    for(var i=0;i<users.length;i++){
        var user_t = users[i];
        $("#myUL").append('<li><a onclick=getUserInfo("'+user_t+'")>'+user_t+'</a></li>');
    }
}