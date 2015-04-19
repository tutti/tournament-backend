<?php

require_once "db.php";

$db = Database::get();
$language = $db->metadata_get("language");
if (!$language) $language = "en";
$db->prepare("get_string", "SELECT translated FROM locale WHERE `language`=:language AND english=:english");
$db->bind("get_string", ":language", $language);

function L($english) {
    global $language, $db;
    if ($language == "en") return $english;
    $db->bind("get_string", ":english", $english);
    try {
        $string = $db->getOne("get_string");
        return $string['translated'];
    } catch (Exception $e) {
        // TODO: Log the lack of a translation for the string.
        return $english;
    }
}