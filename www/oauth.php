<?php
$adapter = $_GET['adapter'];
$domain = $_GET['domain'];
$code = $_GET['code'];

header("location: //$domain/?oauth=$adapter&code=$code");
