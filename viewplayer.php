<?php

require_once "backend/Player.php";
require_once "backend/locale.php";

if (!array_key_exists("popid", $_GET)) {
    echo L("No player specified.");
    die();
}

$player = Player::load($_GET["popid"]);

if (!$player) {
    echo L("Player not found.");
    die();
}

$placements = [];
for ($i = 1; $i <= 3; ++$i) {
    $placements[$i] = $player->getPositionCount($i);
}

// Select an avatar
$gender = ($player->getGender() == "F") ? "f" : "m";
// Note: While the system supports "other" as a gender, there are no sprites for that.
// The sprites are lifted from the pokémon games, and all sprites are male or female there.
$sprite = 0;
if ($placements[1] > 0) {
    $sprite = 2;
}
if ($placements[1] >= 5) {
    $sprite = 3;
}
if ($placements[1] >= 10) {
    $sprite = 4;
}
if ($placements[1] >= 25) {
    $sprite = 5;
}

?>
<!DOCTYPE html>
<html>
    <head>
        <title>Player information</title>
        <link rel="stylesheet" href="style.css" />
    </head>
    <body>
        <div id="trainercard">
            <div id="avatar"><img src="images/avatars/<?= $gender; ?>/<?= $sprite; ?>.png" /></div>
            <div id="name_and_id">
                <span id="name"><?= $player->getName(); ?></span><br />
                <span id="popid"><?= $player->getPopid(); ?></span>
            </div>
            <div class="clearfloat"></div>
            <div id="awards">
                <?php for ($i = 1; $i <= 3; ++$i) { if ($placements[$i] > 0) { ?>
                <div id="award-<?= $i; ?>" class="award">
                    <img src="images/icons/trophy<?= $i; ?>.png" />
                    <?= $placements[$i]; ?>
                </div>
                <?php } } ?>
            </div>
        </div>
    </body>
</html>