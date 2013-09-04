<?php
$adapter = $_GET['adapter'];
$domain = $_GET['domain'];
$code = $_GET['code'];

header("location: //$domain/configure.html?oauth=$adapter&code=$code");
