<?php
    require 'phpMQTT.php';
    require 'config.php';

    $pageName = 'MQTT Message Client';
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title><?php echo $pageName; ?></title>
</head>
<body>
        <?php

    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $message = $_POST['message'];
     
        if (strlen($message) > 500) {
            $message = ($message, 0, 500);
        }

        $client_id = "mqtt-print-publisher";
        $mqtt = new phpMQTT($mqtt_server, $mqtt_port, $client_id);

        if ($mqtt->connect(true, NULL, $mqtt_username, $mqtt_password)) {
	        $mqtt->publish($mqtt_topic, $message, 0);
	        $mqtt->close();
    } else {
        echo "MQTT publish failed!\n";
    }

        ?>

        <script>window.location = "index.php";</script>
        <?php
    }
    else {
        ?>

        <form action="index.php" method="POST">
            Message: <textarea name="message" cols=40 rows=8 maxlength=500><br />
            <input type=submit value="Send Message">
        </form>
    </div>
        <?php
    } ?>
</body>
</html>
