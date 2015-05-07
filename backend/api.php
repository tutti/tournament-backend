<?php

if (!array_key_exists("get", $_GET)) {
    echo '{ "error": "No API function specified - the "get" parameter is missing." }';
    die();
}

switch ($_GET["get"]) {
    case "player":
        break;
    case "tournament":
        break;
}