About this directory
--------------------

This directory contains the file "base.sql" and a series of numbered files, from
"1.sql" and up. Running the database update script will apply all the files that
have yet to be applied, if the current version can be read from the database. If
the version can't be read (usually because the database has not yet been made).

The file "base.sql" will delete any existing data and recreate the empty tables.
All other files will only modify the tables, deleting no data except those found
in columns meant to be discarded.

