<?php

require_once "Player.php";

if (!array_key_exists("popid", $_GET)) {
    echo L("No player specified.");
    die();
}

$player = Player::load($_GET["popid"]);

if (!$player) {
    echo L("Player not found.");
    die();
}