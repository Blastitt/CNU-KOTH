<html>
<?php 
$desiredusername = $_POST["username"];
$desiredpass = $_POST["password"];

require 'dbauth.php';

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("<font color='red'>Connection failed: " . $conn->connect_error . "</font                                                                                                                     >");
}
$sql = "SELECT * from teams WHERE user='" . $desiredusername . "'";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
	if (isset($_POST["password"])) {
	        echo $desiredusername . " is taken at this time";
	}
} else {
	if (isset($_POST["password"])) {
//	$url = 'https://www.google.com/recaptcha/api/siteverify';
///	$data = array('secret' => '6LdWAAgTAAAAAG-WugEwN9GLg07zLtMdGJp2HLzF', 'response' => $_REQUEST["g-recaptcha-response"]);

// use key 'http' even if you send the request to https://...
//		$options = array(
//			'http' => array(
  //				'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
    //   				'method'  => 'POST',
  //      			'content' => http_build_query($data),
//			),
//		);
//		$context  = stream_context_create($options);
//		$result = file_get_contents($url, false, $context);
//			if (strpos($result, "\"success\": true" )) {
//				echo "";
//			} else	{
//				echo "";
//			}
//		echo var_dump($result);
		if (ctype_alnum($desiredusername)) {
		        $sql = "INSERT INTO teams (UserId, user, hash, score) VALUES ('" . rand() . "','" . $desiredusername . "','" . md5($desiredpass) . "','0');";
			$result = $conn->query($sql);
			echo $result;
			echo "Registered " . $desiredusername . " successfully";
		} else {
		die("alphanumeric keys for team name only");
		}
	}
}




?>

<head>
<script src='https://www.google.com/recaptcha/api.js'></script>

<link rel="stylesheet" href="http://yui.yahooapis.com/pure/0.6.0/pure-min.css">

<meta name="viewport" content="width=device-width, initial-scale=1">

		<title>Registration</title>
</head>
<body style="padding-left: 20px ;">
<br><br><br>
<h2>Register here</h2>
<form class="pure-form pure-form-aligned" action="register.php" method="post">
    <fieldset>
        <div class="pure-control-group">
            <label for="name">Username</label>
            <input name="username" id="username" type="text" placeholder="Username" >
        </div>

        <div class="pure-control-group">
            <label for="password">Password</label>
            <input id="password" name="password" type="password" placeholder="Password">
        </div>

<!--	<div class="g-recaptcha" data-sitekey="6LdWAAgTAAAAAAlJDGyQPNVewwWdjS5xARPCA1sv"></div> -->

            <button type="submit" class="pure-button pure-button-primary">Submit</button>
        </div>
    </fieldset>
</form>
</body>
</html>
