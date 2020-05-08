# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id serial PRIMARY KEY,
        start_time timestamp,
        user_id int,
        level text,
        song_id text,
        artist_id text,
        session_id int,
        location text,
        user_agent text
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id int PRIMARY KEY,
        first_name varchar NOT NULL,
        last_name varchar NOT NULL,
        gender char,
        level text
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id text PRIMARY KEY,
        title text NOT NULL,
        artist_id text NOT NULL,
        year int CHECK (year >= 0),
        duration numeric CHECK (duration >= 0)
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id text PRIMARY KEY,
        name varchar NOT NULL,
        location text DEFAULT NULL,
        latitude numeric DEFAULT NULL,
        longitude numeric DEFAULT NULL
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time timestamp PRIMARY KEY,
        hour int CHECK (hour >= 0),
        day int CHECK (day >= 0),
        week int CHECK (week >= 0),
        month int CHECK (month >= 0),
        year int CHECK (year >= 0),
        weekday int CHECK (weekday >= 0));
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
""")

user_table_insert = ("""
    INSERT INTO users 
    VALUES (%s, %s, %s, %s, %s) 
        ON CONFLICT (user_id) 
            DO UPDATE 
                SET level=EXCLUDED.level;
""")

song_table_insert = ("""
    INSERT INTO songs 
    VALUES (%s, %s, %s, %s, %s) 
        ON CONFLICT (song_id) 
            DO NOTHING;
""")

artist_table_insert = ("""
    INSERT INTO artists 
    VALUES (%s, %s, %s, %s, %s) 
        ON CONFLICT (artist_id) 
            DO UPDATE 
                SET location=EXCLUDED.location, latitude=EXCLUDED.latitude, longitude=EXCLUDED.longitude;
""")


time_table_insert = ("""
    INSERT INTO time 
    VALUES (%s, %s, %s, %s, %s, %s, %s) 
        ON CONFLICT (start_time) 
            DO NOTHING;
""")

# FIND SONGS

song_select = ("""
    SELECT S.song_id, A.artist_id 
    FROM songs S JOIN artists A ON S.artist_id = A.artist_id
    WHERE S.title = %s AND A.name = %s AND S.duration = %s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]