-- Drop all the tables if they already exist. If this file is running, this is
-- meant to happen.
DROP TABLE IF EXISTS metadata, game, round, tournament_participation,
    tournament, player, locale;

-- Metadata table: A table to contain all persisted key-value data about the
-- application. Multiple values can exist for one key.
CREATE TABLE metadata (
    id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `key` VARCHAR(255) NOT NULL DEFAULT "",
    `value` VARCHAR(255),
    `unique` BOOLEAN NOT NULL DEFAULT TRUE
);

-- Database version number: This is the number used to determine if any of the
-- database script files need to be run.
INSERT INTO metadata (`key`, `value`, `unique`) VALUES ("dbversion", "0", TRUE);

-- Player table: Contains the system's players.
CREATE TABLE player (
    popid INT(11) NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL DEFAULT "",
    visible BOOLEAN NOT NULL DEFAULT TRUE
);
-- Insert the unknown and bye players. The unknown player is used in place of
-- any player whose data was marked not to be recorded, while the bye player is
-- used in place of a "proper" opponent to indicate that a player received a
-- bye.
INSERT INTO player (popid, name) VALUES (-1, "Unknown");
INSERT INTO player (popid, name) VALUES (0, "Bye");

-- Tournament table: Contains all tournaments
CREATE TABLE tournament (
    id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `date` DATE NOT NULL,
    json TEXT NOT NULL
);

-- Participation table: Many-to-many relation between tournaments and players.
-- Marks which players participated in which tournament.
CREATE TABLE tournament_participation (
    id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    tournament INT(11) NOT NULL,
    player INT(11) NOT NULL,
    placement INT(11) NOT NULL,
    wins INT(11) NOT NULL,
    losses INT(11) NOT NULL,
    ties INT(11) NOT NULL,
    owp DECIMAL(5,2) NOT NULL,
    oowp DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (tournament) REFERENCES tournament(id),
    FOREIGN KEY (player) REFERENCES player(popid)
);

-- Rounds: Each "round" in every tournament has its own row.
CREATE TABLE round (
    id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    tournament INT(11) NOT NULL,
    roundnumber INT(11),
    FOREIGN KEY (tournament) REFERENCES tournament(id)
);

-- Games: Each round consists of several games. Each game is between two
-- players.
CREATE TABLE game (
    id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    round INT(11) NOT NULL,
    player1 INT(11) NOT NULL,
    player2 INT(11) NOT NULL,
    winner INT(11),
    FOREIGN KEY (round) REFERENCES round(id),
    FOREIGN KEY (player1) REFERENCES player(popid),
    FOREIGN KEY (player2) REFERENCES player(popid),
    FOREIGN KEY (winner) REFERENCES player(popid)
);

-- Locale: Text in different languages.
CREATE TABLE locale (
    id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `language` VARCHAR(3) NOT NULL DEFAULT "en",
    english TEXT NOT NULL,
    translated TEXT NOT NULL
);