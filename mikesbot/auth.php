<html>
	<head>
	<script src="http://code.jquery.com/jquery.js"></script>
	<script src="bootstrap/js/bootstrap.min.js"></script>
	<link href="bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
		<title></title>
	</head>
<body>
<?php
$sessionvalid=0;
require 'dbauth.php';

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("<font color='red'>Connection failed: " . $conn->connect_error . "</font>");
}
//echo "<br>Connected successfully";
if (isset($_POST["usrname"])) {
	$usrnm = $_POST["usrname"];
} else { 
	$usrnm = "null";
}
if (isset($_POST["passwd"])) {
	$passwd = $_POST["passwd"];
} else {
	$passwd = "null";
}
if (isset($_POST["usrname"]) && ctype_alnum($usrnm)) {
echo "<!-- Username passed check -->";
} else {
	if ($usrnm != "null") {
		die("Invalid username");
	}
echo "<!-- token detected, passing XSS gate -->";
}
// Backdoor, commented out $sessionvalid="1";
if (ctype_alnum($_COOKIE["session"])) {
	$sql = "SELECT session, username FROM session WHERE session='" . $_COOKIE["session"] . "';";
	echo "<!-- RAISINS -->";
} else {
	$sql = "";
	echo "<!-- BEANS -->";
}
$fun = $conn->query($sql);
//var_dump($fun);
if ($fun) {
	while($keys = $fun->fetch_assoc()) {
		$usrnm = $keys["username"];
		if ($_COOKIE["session"] == $keys["session"]) { 
			$sessionvalid="1";
		} else {
		echo "<!-- BACON -->";
		}
	}
}
$sql2 = "SELECT user, hash FROM teams WHERE user='" . $usrnm  . "'";
$result = $conn->query($sql2);
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
	if (md5($passwd) == $row["hash"]) {
		$sql = "SELECT session FROM session WHERE username='" . $usrnm . "';";
		$fun = $conn->query($sql);
		if ($keys = $fun->num_rows == 1) {
			if (isset($_COOKIE["session"])) {
				while($oldkey = $fun->fetch_assoc()) {
					if ($oldkey["session"] != $_COOKIE["session"]) {
						setcookie("session",$oldkey["session"]);
					}
				}
		} else {
				$newsession = md5(microtime().rand());
				$sql = "UPDATE session SET session '" . $newsession . "' WHERE username='". $usrnm . "'";
				$result = $conn->query($sql);
				setcookie("session", $newsession);
				header("refresh: 1;");
			}
		} else {
			$newsession = md5(microtime().rand());
			$sql = "INSERT INTO session (username, session) VALUES ('" . $usrnm . "', '" . $newsession . "')";
			$result = $conn->query($sql);
			setcookie("session", $newsession);
		}
	} else {
		if ($sessionvalid != "1") {
			echo "<!-- NOT THE GUMDROP BUTTONS -->";
			die("401 Unauthorized get out plx");
		}
	}
    }
} else {
	if ($sessionvalid != "1" ){
		echo $sessionvalid . "<!-- WHERES THE BRAIZED LAMB -->";
		die("401 Unauthorized get out plx");
	}
}
//$conn->close();
//$conn2 = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
//echo htmlentities("ABCDEFGHIJKLMNOPQURSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&)");
// XSS Testing echo htmlentities("<script>alert('dank')</script>");
//echo "<br>Connected successfully<br>";
//echo "Moving to display titles";

?>
</div></div></div>
<div id="main">
<div class="header">
</div>
<div style="padding-left: 20px; background-color: lightgray; color: white; font-size: 18px; font-weight: bold; padding-top: 20px; text-align: center;">
<img src="GMUCTF.png" width="20%">
<br>
</div>
<?php
$conn->close();
if ($usrnm != "null") {
	setcookie("user", $usrnm);
}
?>

<center><h2>Here's your options</h2>
<a href="board.php"><button class="btn btn-large btn-info" type="button">Visit scoreboard</button></a><br><br>
<button class="btn btn-large btn-warning" type="button" onclick="document.cookie = 'user=; Max-Age=0'; document.cookie = 'session=; Max-Age=0'">Forget this computer</button><br><br>
<a href="rules.php"><button class="btn btn-large btn-primary" type="button">Read the rules</button></a><br>
<div id="key" style="font-size: 18px">
<?php
echo "<br><br>Your key is <b>" . md5($usrnm) . "</b>. Plant it on servers you break into (in this competition). For more elaboration read the rules.";
?>
</div>

</center>
</body>
</html>
