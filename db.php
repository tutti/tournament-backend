<?php
require_once "config.php";

class Database {
    private static $object;
    private $db;
    public $queries;
    
    // Metadata queries.
    // Not available to the rest of the database object.
    private $metadata_get;
    private $metadata_new;
    private $metadata_set;
    private $metadata_add;
    private $metadata_remove;
    
    /**
     * Returns a static Database object, creating it if it doesn't exist.
     */
    public static function get()
    {
        if (!self::$object) {
            self::$object = new Database();
        }
        return self::$object;
    }
    
    /**
     * Creates a new Database object.
     * All connection info is defined in config.php.
     */
    public function __construct()
    {
        $host = DBHOST;
        $dbname = DBNAME;
        $this->db = new PDO(
            "mysql:host=$host;dbname=$dbname",
            DBUSER,
            DBPASS
        );
        $this->queries = array();
        
        $this->metadata_get_query = $this->db->prepare("SELECT `value`, `unique` FROM metadata WHERE `key`=:key");
        $this->metadata_new_query = $this->db->prepare("INSERT INTO metadata (`key`, `value`, `unique`) VALUES (:key, :value, :unique)");
        $this->metadata_delete_query = $this->db->prepare("DELETE FROM metadata WHERE `key`=:key");
        $this->metadata_set_query = $this->db->prepare("UPDATE metadata SET `value`=:value WHERE `key`=:key AND `unique`=TRUE");
        $this->metadata_add_query = $this->db->prepare("INSERT INTO metadata (`key`, `value`, `unique`) VALUES (:key, :value, FALSE)");
        $this->metadata_remove_query = $this->db->prepare("DELETE FROM metadata WHERE `key`=:key AND `value`=:value AND `unique`=FALSE");
        $this->metadata_remove_null_query = $this->db->prepare("DELETE FROM metadata WHERE `key`=:key AND `value` IS NULL AND `unique`=FALSE");
    }
    
    /**
     * Prepares a new statement for the given query name.
     * Does not care whether the query name is already in use; if it is
     * the old one is overwritten.
     */
    public function prepare($queryname, $query)
    {
        $sth = $this->db->prepare($query);
        $this->queries[$queryname] = $sth;
    }
    
    /**
     * Binds a parameter value for the given query name.
     */
    public function bind($queryname, $param, $value)
    {
        $sth = $this->queries[$queryname];
        $sth->bindParam($param, $value);
    }
    
    /**
     * Runs the query for the given query name, using the previously
     * bound variables. Returns all rows in the result. Returns an empty
     * variable if there were none.
     */
    public function getAll($queryname)
    {
        $sth = $this->queries[$queryname];
        $sth->execute();
        $sth->setFetchMode(PDO::FETCH_ASSOC);
        $r = array();
        for ($row = $sth->fetch(); $row; $row = $sth->fetch()) {
            $r[] = $row;
        }
        return $r;
    }
    
    /**
     * Runs the query for the given query name, using the previously
     * bound variables. Returns the first row in the result, if there was one.
     * If there were none, false is returned.
     */
    public function getFirst($queryname)
    {
        $sth = $this->queries[$queryname];
        $sth->execute();
        $sth->setFetchMode(PDO::FETCH_ASSOC);
        $row = $sth->fetch();
        if ($row) return $row;
        return false;
    }
    
    /**
     * Runs the query for the given query name, using the previously
     * bound variables. Throws an error if the result doesn't consist of
     * exactly one row. If it does, returns that row.
     */
    public function getOne($queryname)
    {
        $sth = $this->queries[$queryname];
        $sth->execute();
        $sth->setFetchMode(PDO::FETCH_ASSOC);
        $row = $sth->fetch();
        if (!$row) throw new Exception();
        if ($sth->fetch()) throw new Exception();
        return $row;
    }
    
    /**
     * Runs the query, returns nothing.
     */
    public function execute($queryname)
    {
        $sth = $this->queries[$queryname];
        $sth->execute();
    }
    
    public function lastID() {
        return $this->db->lastInsertId();
    }
    
    public function metadata_has_key($key) {
        $this->metadata_get_query->bindParam(":key", $key);
        $this->metadata_get_query->execute();
        $this->metadata_get_query->setFetchMode(PDO::FETCH_ASSOC);
        if ($this->metadata_get_query->fetch()) {
            return true;
        }
        return false;
    }
    
    public function metadata_key_is_unique($key) {
        $this->metadata_get_query->bindParam(":key", $key);
        $this->metadata_get_query->execute();
        $this->metadata_get_query->setFetchMode(PDO::FETCH_ASSOC);
        $row = $this->metadata_get_query->fetch();
        return $row['unique'];
    }
    
    private function metadata_remove_null($key) {
        $this->metadata_remove_null_query->bindParam(":key", $key);
        $this->metadata_remove_null_query->execute();
    }
    
    /**
     * Retrieves metadata based on a key.
     * If a key is marked unique, a single value is returned.
     * If not, then an array of values is returned.
     * All values are always strings.
     */
    public function metadata_get($key) {
        $this->metadata_get_query->bindParam(":key", $key);
        $this->metadata_get_query->execute();
        $this->metadata_get_query->setFetchMode(PDO::FETCH_ASSOC);
        $data = array();
        for ($row = $this->metadata_get_query->fetch(); $row; $row = $this->metadata_get_query->fetch()) {
            $data[] = $row;
        }
        if (count($data) == 0) return null;
        if ($data[0]['unique']) {
            if (count($data) > 1) {
                throw new Exception("Multiple values for unique metadata key");
            }
            return $data[0]['value'];
        }
        $r = array();
        foreach ($data as $num => $row) {
            $r[] = $row['value'];
        }
        return $r;
    }
    
    /**
     * Creates a new metadata key.
     */
    public function metadata_new($key, $value = null, $unique = true) {
        if ($this->metadata_has_key($key)) {
            throw new Exception("Key $key already exists.");
        }
        $this->metadata_new_query->bindParam(":key", $key);
        $this->metadata_new_query->bindParam(":value", $value);
        $this->metadata_new_query->bindParam(":unique", $unique);
        $this->metadata_new_query->execute();
    }
    
    public function metadata_delete($key) {
        if (!$this->metadata_has_key($key)) {
            throw new Exception("Key $key doesn't exist.");
        }
        $this->metadata_delete_query->bindParam(":key", $key);
        $this->metadata_delete_query->execute();
    }
    
    public function metadata_set($key, $value) {
        if (!$this->metadata_has_key($key)) {
            throw new Exception("Key $key doesn't exist.");
        }
        if (!$this->metadata_key_is_unique($key)) {
            throw new Exception("Key $key is not unique.");
        }
        $this->metadata_set_query->bindParam(":key", $key);
        $this->metadata_set_query->bindParam(":value", $value);
        $this->metadata_set_query->execute();
    }
    
    public function metadata_add($key, $value) {
        if (!$this->metadata_has_key($key)) {
            throw new Exception("Key $key doesn't exist.");
        }
        if ($this->metadata_key_is_unique($key)) {
            throw new Exception("Key $key is unique.");
        }
        $this->metadata_remove_null($key);
        $this->metadata_add_query->bindParam(":key", $key);
        $this->metadata_add_query->bindParam(":value", $value);
        $this->metadata_add_query->execute();
    }
    
    public function metadata_remove($key, $value = null) {
        if (!$this->metadata_has_key($key)) {
            throw new Exception("Key $key doesn't exist.");
        }
        if ($this->metadata_key_is_unique($key)) {
            throw new Exception("Key $key is unique.");
        }
        $this->metadata_remove_query->bindParam(":key", $key);
        $this->metadata_remove_query->bindParam(":value", $value);
        $this->metadata_remove_query->execute();
        if (!$this->metadata_has_key($key)) {
            $this->metadata_new($key, null, false);
        }
    }
    
    public function metadata_new_add_or_set($key, $value = null, $unique = true) {
        if ($this->metadata_has_key($key)) {
            if ($this->metadata_key_is_unique($key)) {
                $this->metadata_set($key, $value);
            } else {
                $this->metadata_add($key, $value);
            }
        } else {
            $this->metadata_new($key, $value, $unique);
        }
    }
}