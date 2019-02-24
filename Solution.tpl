
<!DOCTYPE html>
<html lang = "en-us">
<head>
<style>
html * {
  font-family: Tahoma !important;
  font-size: 20px;
}
p {
  border: 1px solid dodgerblue;
  padding: 30px;
  margin: 25px;
}
a {
  color: #17FFA3;
  font-size: 16px;
  padding: 10px;
}
body {background-color: white;
  background-image: url("Road.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
  color: white;
}
h1   {color: blue;}
</style>
<title>TrafficBGone</title>
<a href="Home.html">Home Page</a>     <a href="Rewards.html">Rewards</a>
</head>
    <h1>Time to Destination {{timeToDest}}!</h1>
    <img src="static/ride.png">
    <p>Depature Time: {{departureTime}}</p>
    <p>Arrival Time: {{arrivalTime}}</p>
    <p>Points earned {{points}}</p>
<div class="right"><div class="gmap_canvas"><iframe width="706" height="250" id="gmap_canvas" src="https://maps.google.com/maps?q=Eisenhower%20Tunnel&t=&z=9&ie=UTF8&iwloc=&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe><a href="https://www.jetzt-drucken-lassen.de">website</a></div><style>.mapouter{text-align:right;height:250px;width:706px;}.gmap_canvas {overflow:hidden;background:none!important;height:250px;width:706px;}</style>Google Maps by <a href="https://www.embedgooglemap.net" rel="nofollow" target="_blank">Embedgooglemap.net</a></div>
</html>
