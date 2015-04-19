<?php

require_once "../db.php";
require_once "../locale.php";
    
$user = DBUSER;
$pass = DBPASS;
$dbname = DBNAME;
$host = DBHOST;

if (array_key_exists('reset', $_POST)) {
    echo L("Running database setup file") . "<br />";
    $command = "mysql -u$user -p$pass -h $host -D $dbname < base.sql";
    shell_exec($command);
}

try {
    $db = Database::get();
    
    $dbversion = $db->metadata_get("dbversion");
    if ($dbversion == null) {
        // Go to exception handler
        throw new Exception();
    }
    
    for ($i = $dbversion + 1; file_exists($i.".sql"); ++$i) {
        echo L("Running database update file") . " $i";
        $command = "mysql -u$user -p$pass -h $host -D $dbname < $i.sql";
        
        $output = shell_exec($command);
        
        echo $output;
        echo "<br />";
    }
    
    echo L("Database up to date.");
} catch (Exception $e) {
    echo L("Could not connect. Reset database to defaults?") . "<br />";
    echo '<form method="post" action="update.php">';
    echo "<button id='reset' name='reset' value='reset'>" . L("Reset") . "</button>";
    echo "</form>";
}