## Database Setup
I created a database setup script so the database can be reset easily. 
The script drops the existing nc_plus_one database if it exists, then recreates it.

## Database Connection
I created a reusable get_connection function inside db/connection.py. It uses psycopg2.connect to connect to the nc_plus_one database. For now, the database name is stored in db/credentials.py, which has been added to .gitignore so local credentials are not committed. The connection can now be imported and used from another file, such as seed.py.


## Database Seeding

The project uses a seed script to create a clean version of the database with test data.

The database schema is stored in `db/schema.sql`. It drops and recreates the `users`, `venues`, `events`, and `rsvps` tables in the correct order so key relationships work correctly.

The `db/seed.py` file reads the JSON files in `db/data` and bulk inserts the users, venues, events, and RSVP records into the database. This means the database can be reset to the same starting data whenever needed.

To run the seed:

bash
python db/seed.py





I ordered the events by the latest events first so at ascending so the API returns them in chronological order, with the earliest event first. This is useful for an events list.