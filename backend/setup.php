<?php

require_once "db.php";
require_once "locale.php";

$db = Database::get();
$dbversion = null;
try {
    $dbversion = $db->metadata_get("dbversion");
} catch (Exception $e) {
    $dbversion = null;
}

if ($dbversion == null) {
    echo sprintf(L("You need to run %sthe database script%s first. Come back here after."), '<a href="sql/update.php">', "</a>");
    die();
}

if (array_key_exists("setup", $_POST)) {
    try {
        if (!$db->metadata_has_key("admin_username")) $db->metadata_new("admin_username", $_POST['admin_username']);
        if (!$db->metadata_has_key("admin_password")) $db->metadata_new("admin_password", password_hash($_POST['admin_password'], PASSWORD_DEFAULT));
        if (!$db->metadata_has_key("admin_playerid")) $db->metadata_new("admin_playerid", $_POST['admin_playerid']);
        $db->metadata_new_add_or_set("language", $_POST["language"]);
        echo L("Setup complete.");
        die();
    } catch (Exception $e) {
        echo L("Something went wrong. The database seems corrupt.");
        die();
    }
}

$languages = $db->metadata_get("languages");
if (!$languages) $languages = [];

?>

<!DOCTYPE html>
<html>
    <head>
        <title><?= L("Tournament backend install script"); ?></title>
        <link rel="stylesheet" href="style.css" />
    </head>
    <body>
        <h2><?= L("Tournament backend install script"); ?></h2>
        <?= L("Please enter the following details, then hit Submit."); ?>
        <form method="post" action="setup.php">
            <?php if (!$db->metadata_has_key("admin_username")) {?><label for="admin_username"><?= L("Admin username"); ?>: </label><input type="text" name="admin_username" /><br /><?php } ?>
            <?php if (!$db->metadata_has_key("admin_password")) {?><label for="admin_password"><?= L("Admin password"); ?>: </label><input type="password" name="admin_password" /><br /><?php } ?>
            <?php if (!$db->metadata_has_key("admin_playerid")) {?><label for="admin_playerid"><?= L("Admin player ID"); ?>: </label><input type="number" name="admin_playerid" /><br /><?php } ?>
            <label for="language"><?= L("Language"); ?>: </label>
            <select name="language">
                <option value="en">English</option>
                <?php foreach ($languages as $language) {
                echo "<option value=\"$language\">".$db->metadata_get("language_$language")."</option>";
                } ?>
            </select>
            <br />
            <button name="setup" value="setup"><?= L("Submit"); ?></button>
        </form>
    </body>
</html>