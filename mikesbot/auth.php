<html>
	<head>
		<title><?php $_POST["usrname"]; ?></title>
	<script src="ui.js"></script>
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
$usrnm = $_POST["usrname"];
$passwd = $_POST["passwd"];
if (ctype_alnum($usrnm)) {
echo "Valid";
} else {
die("Invalid username");
}
$sql = "SELECT session FROM session WHERE username='" . $usrnm . "';";
$fun = $conn->query($sql);
while($keys = $fun->fetch_assoc()) {
	if (isset($_COOKIE["session"])) { 
		$sessionvalid="1";
	} else {
//		die("Tet");
	}
}
$sql = "SELECT user, hash FROM teams WHERE user='" . $usrnm  . "'";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
//	echo $row["hash"] . $passwd;
 //       echo "<br>Logging in with " . $row["username"];
	if (md5($passwd) == $row["hash"]) {
		// echo "<br>Authenticated as " . $row["username"];
	// echo "Auth valid";
		$sql = "SELECT session FROM session WHERE username='" . $usrnm . "';";
		$fun = $conn->query($sql);
		if ($keys = $fun->num_rows == 1) {
			if (isset($_COOKIE["session"])) {
	//			die($keys["session"]);
		} else {
		//		echo "B";
				$newsession = md5(microtime().rand());
				echo $newsession;
				$sql = "UPDATE session SET session '" . $newsession . "' WHERE username='". $usrnm . "'";
		//		echo $sql;
				$result = $conn->query($sql);
				setcookie("session", $newsession);
			}
		} else {
			$newsession = md5(microtime().rand());
			//echo 
			$sql = "INSERT INTO session (username, session) VALUES ('" . $usrnm . "', '" . $newsession . "')";
			$result = $conn->query($sql);
			setcookie("session", $newsession);
		}
//	echo "Moving on";
	} else {
		if ($sessionvalid != "1") {
			die("401 Unauthorized get out plx");
		}
	}
    }
} else {
    // echo "0 usernames in DB, somehow, idk how, I'm just the computer man";
    die("401 Unauthorized get out plx");
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
<h2>Announcements</h2>
</div><div class="content">
<?php

$sql = "SELECT announcement, announcer FROM announcements";
$announcements = $conn->query($sql);
if ($announcements->num_rows > 0) {
		while($announce = $announcements->fetch_assoc()) {
			echo "<br><b>" . htmlentities($announce["announcer"]) . "</b>: " . htmlentities($announce["announcement"]);
		}
}


$conn->close();
setcookie("user", $usrnm);
?>
</div>


<font size="5">BEANS</font>





</body>
</html>
