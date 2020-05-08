import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

ARN = config.get('IAM_ROLE', 'ARN')

LOG_DATA = config.get('S3', 'LOG_DATA')
LOG_JSONPATH = config.get('S3', 'LOG_JSONPATH')
SONG_DATA =  config.get('S3', 'SONG_DATA')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events (
        artist text,
        auth text,
        firstName text,
        gender char,
        itemInSession int,
        lastName text,
        length numeric,
        level text,
        location text,
        method text,
        page text,
        registration numeric,
        sessionId int,
        song text,
        status int,
        ts timestamp,
        userAgent text,
        userId int
    );
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
        num_songs int,
        artist_id text,
        artist_latitude numeric,
        artist_longitude numeric,
        artist_location text,
        artist_name text, 
        song_id text,
        title text,
        duration numeric,
        year int
    );
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id int IDENTITY(0,1) PRIMARY KEY,
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
        first_name text,
        last_name text,
        gender char,
        level text
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id text PRIMARY KEY,
        title text,
        artist_id text,
        year int,
        duration numeric
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id text PRIMARY KEY,
        name text,
        location text,
        latitude numeric,
        longitude numeric
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time timestamp PRIMARY KEY,
        hour int,
        day int,
        week int,
        month int,
        year int,
        weekday int
    );
""")

# STAGING TABLES

staging_events_copy = ("""
    copy staging_events from {}
    credentials 'aws_iam_role={}'
    compupdate off region 'us-west-2'
    timeformat as 'epochmillisecs'
    format as json {};
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
    copy staging_songs from {}
    credentials 'aws_iam_role={}'
    compupdate off region 'us-west-2'
    format as json 'auto';
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT to_timestamp(to_char(e.ts, '9999-99-99 99:99:99'), 'YYYY-MM-DD HH24:MI:SS'),
                    e.userId AS user_id,
                    e.level,
                    s.song_id,
                    s.artist_id,
                    e.sessionId AS session_id,
                    e.location,
                    e.userAgent AS user_agent
    FROM staging_events e
    JOIN staging_songs s ON (s.title = e.song AND s.artist_name = e.artist);
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT userId AS user_id,
                    firstName AS first_name,
                    lastName AS last_name,
                    gender,
                    level
    FROM staging_events
    WHERE userID IS NOT NULL;
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT DISTINCT song_id,
                    title,
                    artist_id,
                    year,
                    duration
    FROM staging_songs
    WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT artist_id,
                    artist_name AS name,
                    artist_location AS location,
                    artist_latitude AS latitude,
                    artist_longitude AS longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT ts AS start_time,
                    EXTRACT(hour FROM ts),
                    EXTRACT(day FROM ts),
                    EXTRACT(week FROM ts),
                    EXTRACT(month FROM ts),
                    EXTRACT(year FROM ts),
                    EXTRACT(weekday FROM ts)
    FROM staging_events
    WHERE ts IS NOT NULL;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
