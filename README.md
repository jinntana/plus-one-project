I created a database setup script so the database can be reset easily. 
The script drops the existing nc_plus_one database if it exists, then recreates it.


I created a reusable get_connection function inside db/connection.py. It uses psycopg2.connect to connect to the nc_plus_one database. For now, the database name is stored in db/credentials.py, which has been added to .gitignore so local credentials are not committed. The connection can now be imported and used from another file, such as seed.py.