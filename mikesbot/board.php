
<!DOCTYPE html>
<html>
  <head>
	<meta http-equiv="refresh" content="30">
    <title>Scoreboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
  </head>
  <body style="background-image: url('');">
    <script src="http://code.jquery.com/jquery.js"></script>
    <script src="bootstrap/js/bootstrap.min.js"></script>

<div style="padding-left: 20px; background-color: lightgray; color: white; font-size: 18px; font-weight: bold; padding-top: 20px; text-align: center;">
<img src="GMUCTF.png" width="20%"></img>
<br>
</div>

<container>
<table class="table" style="width: 70%; margin-left: auto; margin-right: auto"">
<tr><th>Name</th><th>Score</th></tr>
<?php

require 'dbauth.php';
$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("<font color='red'>Connection failed: " . $conn->connect_error . "</font>");
}

$sql = "SELECT user, score FROM teams";
$result = $conn->query($sql);
    while($row = $result->fetch_assoc()) {
		 $scores[] = $row['score'];
		 $users[] = $row['user'];
}
// DEBUG var_dump($scores);
//var_dump($users);
if (isset($_COOKIE["user"])) {
	echo "<center><br>You look like you're " . $_COOKIE["user"] . ", who has a score of: <br>" ;
	$keyloc = array_search($_COOKIE["user"] , $users);
	echo "<b>" . $scores[$keyloc] . "</b></center><br>";
}

foreach($scores as $key => $item){
  print "<tr><td>" . $users[$key] . "</td><td>" . $item . "</td></tr>";
}
?>


</table>
<container>
<center>
<iframe src="log.log" width="90%" scrolling="yes" style="text-align: yes" />
</center>




</body></html>
