<?php

require_once "db.php";
require_once "Player.php";

class Tournament {
    
    private static $has_init = false;
    private static $db;
    
    private $id;
    private $players;
    private $rounds;
    private $results;
    
    private static function __init() {
        if (self::$has_init) return;
        
        self::$db = Database::get();
        self::$db->prepare("save_tournament", "INSERT INTO tournament (`date`, json) VALUES (:date, :json)");
        self::$db->prepare("create_round", "INSERT INTO round (tournament, roundnumber) VALUES (:tournamentid, :roundnumber)");
        self::$db->prepare("create_game", "INSERT INTO game (round, player1, player2, winner) VALUES (:roundid, :p1id, :p2id, :wid)");
        self::$db->prepare("create_participation", "INSERT INTO tournament_participation (tournament, player, placement, wins, losses, ties, owp, oowp) VALUES (:tournamentid, :playerid, :placement, :wins, :losses, :ties, :owp, :oowp)");
        
        self::$has_init = true;
    }
    
    public static function create($date, $json) {
        self::__init();
        // Create the tournament record
        self::$db->bind("save_tournament", ":date", $date);
        self::$db->bind("save_tournament", ":json", $json);
        self::$db->execute("save_tournament");
        $tournament_id = self::$db->lastID();
        self::$db->bind("create_round", ":tournamentid", $tournament_id);
        self::$db->bind("create_participation", ":tournamentid", $tournament_id);
        
        $tournament = new Tournament();
        $tournament->id = $tournament_id;
        
        // Turn the JSON data into an array
        $data = json_decode($json, true);
        
        // Get player objects for all participants
        $tournament->players = [];
        foreach ($data['players'] as $popid => $name) {
            $tournament->players[$popid] = Player::create_or_load($popid, $name);
        }
        foreach ($data['droppedPlayers'] as $popid => $name) {
            $tournament->players[$popid] = Player::create_or_load($popid, $name);
        }
        
        $tournament->rounds = [];
        // Loop through the rounds
        for ($roundnum = 0; $roundnum < count($data['rounds']); ++$roundnum) {
            // Insert a round record into the database
            self::$db->bind("create_round", ":roundnumber", $roundnum+1);
            self::$db->execute("create_round");
            $round_id = self::$db->lastID();
            self::$db->bind("create_game", ":roundid", $round_id);
            
            $tournament->rounds[$roundnum] = [];
            // Loop through the games in the round
            foreach ($data['rounds'][$roundnum] as $game) {
                $p1 = ($game['p1'] < 0) ? -1 : $game['p1'];
                $p2 = ($game['p2'] < 0) ? -1 : $game['p2'];
                
                $gamedata = [
                    'player1' => Player::load($p1),
                    'player2' => Player::load($p2),
                ];
                
                self::$db->bind("create_game", ":p1id", $p1);
                self::$db->bind("create_game", ":p2id", $p2);
                if (array_key_exists('winner', $game)) {
                    self::$db->bind("create_game", ":wid", $game['winner']);
                    $gamedata['winner'] = Player::load($game['winner']);
                } else {
                    self::$db->bind("create_game", ":wid", null);
                    $gamedata['tie'] = true;
                }
                self::$db->execute("create_game");
                
                $tournament->rounds[$roundnum][] = $gamedata;
                
            }
        }
        
        $tournament->results = [];
        // Create participation objects for all players who finished
        for ($i = 0; $i < count($data['results']); ++$i) {
            $result = $data['results'][$i];
            if ($result['id'] < 0) continue;
            $placement = $i + 1;
            $tournament->results[$i] = [];
            $tournament->results[$i]['player'] = Player::load($result['id']);
            $tournament->results[$i]['placement'] = $placement;
            $tournament->results[$i]['wins'] = $result['wins'];
            $tournament->results[$i]['losses'] = $result['losses'];
            $tournament->results[$i]['ties'] = $result['ties'];
            $tournament->results[$i]['owp'] = $result['owp'];
            $tournament->results[$i]['oowp'] = $result['oowp'];
            self::$db->bind("create_participation", ":playerid", $result['id']);
            self::$db->bind("create_participation", ":placement", $placement);
            self::$db->bind("create_participation", ":wins", $result['wins']);
            self::$db->bind("create_participation", ":losses", $result['losses']);
            self::$db->bind("create_participation", ":ties", $result['ties']);
            self::$db->bind("create_participation", ":owp", $result['owp']);
            self::$db->bind("create_participation", ":oowp", $result['oowp']);
            self::$db->execute("create_participation");
        }
        
        print_r($tournament);
    }
    
    public static function load($id) {
        self::__init();
    }
    
}

?>