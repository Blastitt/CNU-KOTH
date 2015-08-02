<html>
<head>
</head>
<body>

<?php

$result = shell_exec("/servicechk.sh");

if ($result == 0) {
	echo "<img src='BURRR.png' width='90%'></img>";
}
if ($result == 1) {
	echo "<img src='BURRRR.png' width='90%'></img>";
}
?>
</body>
</html>
