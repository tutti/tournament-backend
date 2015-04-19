<?php

require_once "db.php";
require_once "locale.php";
require_once "Tournament.php";

$db = Database::get();

if (array_key_exists("upload", $_POST)) {
    $admin_username = $db->metadata_get("admin_username");
    $admin_passhash = $db->metadata_get("admin_password");
    if ($_POST['user'] != $admin_username || !password_verify($_POST['pass'], $admin_passhash)) {
        echo L("Incorrect username or password.");
        die();
    }
    
    $text = file_get_contents($_FILES['file']['tmp_name']);
    
    $data = json_decode($text, true);
    if (!$data) {
        echo L("Invalid file.");
        die();
    }
    
    $tournament = Tournament::create($_POST['date'], $text);
    
    echo L("Tournament uploaded.");
    die();
}

?>

<!DOCTYPE html>
<html>
    <head>
        <title><?= L("Upload tournament file"); ?></title>
        <link rel="stylesheet" href="style.css" />
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
        <link rel="stylesheet" href="jquery.timelord.css" />
        <script src="jquery.timelord.js"></script>
        <script>
            (function($) {
                $(document).ready(function() {
                    $("input#date").timelord("replace", "Datepicker");
                    $.timelord("option", "formatDate", "{ year }-{ month.zeropad2 }-{ day.zeropad2 }");
                })
            })(jQuery);
        </script>
    </head>
    <body>
        <h2><?= L("Upload tournament file"); ?></h2>
        <form action="upload.php" method="post" enctype="multipart/form-data">
            <label for="user"><?= L("Username"); ?>: </label><input type="text" name="user" /><br />
            <label for="pass"><?= L("Password"); ?>: </label><input type="password" name="pass" /><br />
            <label for="file"><?= L("File"); ?>: </label><input type="file" name="file" /><br />
            <label for="date"><?= L("Date"); ?>: </label><input type="text" name="date" id="date" /><br />
            <button name="upload" value="upload"><?= L("Upload"); ?></button>
        </form>
    </body>
</html>