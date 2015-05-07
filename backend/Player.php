<?php

require_once "db.php";

class Player {
    
    private static $has_init = false;
    private static $db;
    private static $players = [];
    
    private $popid;
    private $name;
    private $gender;
    private $visible;
    
    private static function __init() {
        if (self::$has_init) return;
        
        self::$db = Database::get();
        self::$db->prepare("create_player", "INSERT INTO player (popid, name, visible) VALUES (:popid, :name, true)");
        self::$db->prepare("get_player", "SELECT * FROM player WHERE popid=:popid");
        self::$db->prepare("get_position_count", "SELECT count(*) AS count FROM tournament_participation WHERE player=:popid AND placement=:position");
        self::$db->prepare("get_staff_positions", "SELECT count(*) AS count FROM tournament_staff WHERE player=:popid");
        
        self::$has_init = true;
    }
    
    public static function create($popid, $name) {
        self::__init();
        
        self::$db->bind("create_player", ":popid", $popid);
        self::$db->bind("create_player", ":name", $name);
        
        if ($popid >= 0) {
            try {
                self::$db->execute("create_player");
            } catch (Exception $e) {
                throw new Exception("Player already exists.");
            }
        }
        
        $player = new Player();
        $player->popid = $popid;
        $player->name = $name;
        $player->gender = "M";
        $player->visible = true;
        self::$players[$popid] = $player;
        
        return $player;
    }
    
    public static function load($popid) {
        self::__init();
        
        if (array_key_exists($popid, self::$players)) {
            return self::$players[$popid];
        }
        
        self::$db->bind("get_player", ":popid", $popid);
        try {
            $data = self::$db->getOne("get_player");
        } catch (Exception $e) {
            return null;
        }
        
        $player = new Player();
        $player->popid = $popid;
        $player->name = $data['name'];
        $player->gender = $data['gender'];
        $player->visible = $data['visible'];
        self::$players[$popid] = $player;
        
        return $player;
    }
    
    public static function create_or_load($popid, $name) {
        self::__init();
        
        if (array_key_exists($popid, self::$players)) {
            return self::$players[$popid];
        }
        
        $player = self::load($popid);
        if ($player) return $player;
        
        return self::create($popid, $name);
    }
    
    public function getPopid() {
        return $this->popid;
    }
    
    public function setName($name) {
        $this->name = $name;
    }
    
    public function getName() {
        return $this->name;
    }
    
    public function setGender($gender) {
        if ($gender != "M" && $gender != "F" && $gender != "O") {
            return;
        }
        $this->gender = $gender;
    }
    
    public function getGender() {
        return $this->gender;
    }
    
    public function getPositionCount($position) {
        self::$db->bind("get_position_count", ":popid", $this->popid);
        self::$db->bind("get_position_count", ":position", $position);
        $count = self::$db->getFirst("get_position_count");
        return $count['count'];
    }
    
    public function isStaff() {
        self::$db->bind("get_staff_positions", ":popid", $this->popid);
        $count = self::$db->getFirst("get_staff_positions");
        return ($count['count'] > 0);
    }
}
