DELETE FROM metadata WHERE `key`="languages" AND `value`="no";
DELETE FROM metadata WHERE `key`="language_no";

INSERT INTO metadata (`key`, `value`, `unique`) VALUES ("languages", "no", FALSE);
INSERT INTO metadata (`key`, `value`, `unique`) VALUES ("language_no", "Norsk", TRUE);

DELETE FROM locale WHERE `language`="no";

INSERT INTO locale (`language`, english, translated) VALUES
    ("no", "Running database setup file", "Kj�rer databaseinstalleringsfil"),
    ("no", "Running database update file", "Kj�rer databaseoppdateringsfil"),
    ("no", "Database up to date.", "Databasen er oppdatert."),
    ("no", "Could not connect. Reset database to defaults?", "Kunne ikke hente data. Tilbakestill?"),
    ("no", "Reset", "Tilbakestill"),
    ("no", "You need to run %sthe database script%s first. Come back here after.", "Du m� kj�re %sdatabaseskriptet%s f�rst. Kom tilbake hit etterp�."),
    ("no", "Setup complete.", "Installering fullf�rt."),
    ("no", "Something went wrong. The database seems corrupt.", "Noe gikk galt. Databasen ser ut til � v�re korrupt."),
    ("no", "Tournament backend install script", "Turneringsserver: Installasjonsskript"),
    ("no", "Please enter the following details, then hit Submit.", "Fyll inn disse detaljene, og trykk Send."),
    ("no", "Admin username", "Admins brukernavn"),
    ("no", "Admin password", "Admins passord"),
    ("no", "Admin player ID", "Admins spiller-ID"),
    ("no", "Language", "Spr�k"),
    ("no", "Submit", "Send"),
    ("no", "Upload tournament file", "Last opp turneringsfil"),
    ("no", "Username", "Brukernavn"),
    ("no", "Password", "Passord"),
    ("no", "File", "Fil"),
    ("no", "Upload", "Last opp"),
    ("no", "Incorrect username or password.", "Feil brukernavn eller passord."),
    ("no", "Invalid file.", "Ugyldig fil."),
    ("no", "Tournament uploaded.", "Turnering lagret.")
;