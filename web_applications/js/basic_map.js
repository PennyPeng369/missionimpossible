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
var pre_index;
var tweetData = [];
var overlaySet = [];
function initMap()
{
    map = new google.maps.Map(document.getElementById('map_home'), {
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
    url:'/streams',
    type: 'GET', 
    contentType:'application/json',
    dataType:'json',
    }).done(function (res) {
    
   // console.log(res);
    pre_index = res.num;
    tweetData = res.data;
    d3show(tweetData);
    

    });

    //var sec = Math.round(Math.random()*90+60); 
    var sec = 10;  
    window.setInterval(getNewTweet, 1000*sec);   
}

function transformTweet(data){
  var text_string ='';
  for(var i =0; i<data.length; i++){
    var text = data[i].text;
    text_string += text;
  }
  return text_string;
}

function getNewTweet(){
  var getData = $.ajax({
    url:'/streams/change',
    type: 'POST', 
    data:JSON.stringify({
      pre_index:pre_index
    }),
    contentType:'application/json',
    dataType:'json',
    }).done(function (res) {
    
  //  console.log(res);
    pre_index += res.length;
    var data = res;
    for(var i=0; i<data.length; i++){
      tweetData.push(data[i]);
    }
    d3show(tweetData);
    
    });
}

function d3show(data){
   // console.log(data.length);
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
                    .data(data)
                    .each(transform)
                    .enter()
                    .append("svg")
                    .each(transform);

                var r =4;
                

                marker.append("circle")
                    .attr("cx",padding)
                    .attr("cy",padding)
                    .attr("r",r)
                    .attr("stroke","#3366cc")
                    .attr("stroke-opacity",1.0)
                    .attr("stroke-width","2px")
                    .attr("fill","#3366cc")
                    .attr("fill-opacity",0.6);
          

                    function transform(d){
                    d = new google.maps.LatLng(d.lat,d.lng);
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

     overlay.setMap(map);
     //setOverlay(map);
     var text_string = transformTweet(data);
    drawWordCloud(text_string);

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
