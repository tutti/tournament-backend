<?php

require_once "../db.php";

// This file, being the locale setup file, does not itself use locales.

$user = DBUSER;
$pass = DBPASS;
$dbname = DBNAME;
$host = DBHOST;

try {
    $db = Database::get();
    
    $dbversion = $db->metadata_get("dbversion");
    if ($dbversion == null) {
        echo "Could not connect to the database.";
        die();
    }
    
    $dir = opendir(".");
    $file = readdir($dir);
    while ($file !== false) {
        if ($file == "update.php" || substr($file, 0, 1) == ".") {
            $file = readdir($dir);
            continue;
        }
        
        $command = "mysql -u$user -p$pass -h $host -D $dbname < $file";
        $output = shell_exec($command);
        $file = readdir($dir);
    }
    
    echo "Languages installed.";
} catch (Exception $e) {
    echo "Could not connect to the database.";
}