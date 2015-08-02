<?php

if ($_GET["token"] == "dd662924a075309a141ef0ae2bd46daa") {
	echo "Ayyy";
} else {
	die("invalid");
}

require 'dbauth.php';
$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("<font color='red'>Connection failed: " . $conn->connect_error . "</font>");
}

//$conn = mysql_query("SELECT user FROM 'teams'");

$sql = "SELECT user FROM teams";
$result = $conn->query($sql);
    while($row = $result->fetch_assoc()) {
     //   if ($_COOKIE["session"] == $row["session"]) {
     //           $sessionlive= "TRUUUUUU";
   //             $userloggedin = $row["username"];
//              echo $userloggedin  . " detected";
       // }
   // }
       // if ($sessionlive == false) {
     //           die("I HAZ NO SESSION, WHERE IZ SESSIN B");
	 $inspector[] = $row['user'];
}
print_r($inspector);
foreach ($inspector as $teamname) {
	$scoar = shell_exec("/checkteam.sh " . md5($teamname));
	$sql2 = "SELECT score FROM teams WHERE user='" . $teamname . "';";
	$result3 = $conn->query($sql2);
	echo $scoar;
	while ($row = $result3->fetch_assoc()) {
        $scoreorig = $row['score'];
    	}
	$newscore = $scoreorig+$scoar;
	echo $newscore . " new score, " . $scoreorig . " old score";
	$sql3 = "UPDATE teams SET score='" . $newscore .  "' WHERE user='" . $teamname .  "'";
	$result4 = $conn->query($sql3);
}

?>
