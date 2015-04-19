DELETE FROM metadata WHERE `key`="languages" AND `value`="no";
DELETE FROM metadata WHERE `key`="language_no";

INSERT INTO metadata (`key`, `value`, `unique`) VALUES ("languages", "no", FALSE);
INSERT INTO metadata (`key`, `value`, `unique`) VALUES ("language_no", "Norsk", TRUE);

DELETE FROM locale WHERE `language`="no";

INSERT INTO locale (`language`, english, translated) VALUES
    ("no", "Running database setup file", "Kjører databaseinstalleringsfil"),
    ("no", "Running database update file", "Kjører databaseoppdateringsfil"),
    ("no", "Database up to date.", "Databasen er oppdatert."),
    ("no", "Could not connect. Reset database to defaults?", "Kunne ikke hente data. Tilbakestill?"),
    ("no", "Reset", "Tilbakestill"),
    ("no", "You need to run %sthe database script%s first. Come back here after.", "Du må kjøre %sdatabaseskriptet%s først. Kom tilbake hit etterpå."),
    ("no", "Setup complete.", "Installering fullført."),
    ("no", "Something went wrong. The database seems corrupt.", "Noe gikk galt. Databasen ser ut til å være korrupt."),
    ("no", "Tournament backend install script", "Turneringsserver: Installasjonsskript"),
    ("no", "Please enter the following details, then hit Submit.", "Fyll inn disse detaljene, og trykk Send."),
    ("no", "Admin username", "Admins brukernavn"),
    ("no", "Admin password", "Admins passord"),
    ("no", "Admin player ID", "Admins spiller-ID"),
    ("no", "Language", "Språk"),
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