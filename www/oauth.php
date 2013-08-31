<?php
$adapter = $_GET['adapter'];
$domain = $_GET['domain'];
$code = $_GET['code'];

header("location: /configure.html?oauth=vk.com&code=$code");
