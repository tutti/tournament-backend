<?php

require_once "db.php";

$keylist = [
    // "key" => <key has unique value>
    "dbversion" => true
];

$db = Database::get();
?>
<!DOCTYPE html>
<html>
    <head>
        <title>Metadata overview</title>
        <style>
            table {
                border-collapse: collapse;
            }
            td, th {
                border: 1px solid black;
            }
        </style>
    </head>
    <body>
        <h2>Metadata</h2>
        <table>
            <thead>
                <tr>
                    <th>Key</th>
                    <th>Value(s)</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($keylist as $key => $unique) { ?><tr>
                    <td><?= $key; ?></td>
                    <td>
                        <?php
                        if ($unique) {
                            echo $db->metadata_get($key);
                        } else {
                            foreach ($db->metadata_get($key) as $value) {
                                echo $value;
                                echo "<br />";
                            }
                        } ?>
                    </td>
                </tr><?php } ?>
            </tbody>
        </table>
    </body>
</html>