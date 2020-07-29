import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
LOG_DATA = config.get('S3', 'LOG_DATA')
LOG_JSONPATH = config.get('S3', 'LOG_JSONPATH')
SONG_DATA = config.get('S3', 'SONG_DATA')
ARN = config.get('IAM_ROLE', 'ARN')

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
        artist           VARCHAR,
        auth             VARCHAR,
        firstName        VARCHAR,
        gender           VARCHAR,
        itemInSession    VARCHAR,
        lastName         VARCHAR,
        length           DOUBLE PRECISION,
        level            VARCHAR,
        location         VARCHAR,
        method           VARCHAR,
        page             VARCHAR,
        registration     DOUBLE PRECISION,
        sessionId        VARCHAR,
        song             VARCHAR,
        status           VARCHAR,
        ts               BIGINT,
        userAgent        VARCHAR,
        userId           VARCHAR
    );
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
        num_songs        INTEGER,
        artist_id        VARCHAR,
        artist_latitude  DOUBLE PRECISION,
        artist_longitude DOUBLE PRECISION,
        artist_location  VARCHAR,
        artist_name      VARCHAR,
        song_id          VARCHAR,
        title            VARCHAR,
        duration         DOUBLE PRECISION,
        year             SMALLINT
    );
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id     INTEGER    IDENTITY(0,1) PRIMARY KEY,
        start_time      TIMESTAMP  DISTKEY SORTKEY,
        user_id         VARCHAR,
        level           VARCHAR,
        song_id         VARCHAR,
        artist_id       VARCHAR,
        session_id      VARCHAR,
        location        VARCHAR,
        user_agent      VARCHAR 
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id        VARCHAR PRIMARY KEY SORTKEY,
        first_name     VARCHAR,
        last_name      VARCHAR,
        gender         VARCHAR,
        level          VARCHAR
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id        VARCHAR PRIMARY KEY SORTKEY,
        title          VARCHAR,
        artist_id      VARCHAR,
        year           SMALLINT,
        duration       DOUBLE PRECISION
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id      VARCHAR PRIMARY KEY SORTKEY,
        name           VARCHAR,
        location       VARCHAR,
        latitude       DOUBLE PRECISION,
        longitude      DOUBLE PRECISION
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time     TIMESTAMP PRIMARY KEY SORTKEY DISTKEY,
        hour           SMALLINT,
        day            SMALLINT,
        week           SMALLINT,
        month          SMALLINT,
        year           SMALLINT,
        weekday        SMALLINT
    );
""")

# STAGING TABLES

staging_events_copy = ("""
    copy staging_events from {}
    credentials 'aws_iam_role={}'
    region 'us-west-2'
    format as JSON {}
    timeformat as 'epochmillisecs';
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
    copy staging_songs from {}
    credentials 'aws_iam_role={}'
    region 'us-west-2'
    format as JSON 'auto';
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT TIMESTAMP 'epoch' + e.ts / 1000 * INTERVAL '1 second' AS start_time, 
           e.userId, 
           e.level, 
           s.song_id, 
           s.artist_id, 
           e.sessionId, 
           e.location, 
           e.userAgent
    FROM staging_events e
    JOIN staging_songs s ON e.song = s.title AND e.artist = s.artist_name
    WHERE e.page = 'NextSong';
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT userId,
           firstName,
           lastName, 
           gender, 
           level
    FROM staging_events
    WHERE userId IS NOT NULL;
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
           artist_name, 
           artist_location, 
           artist_latitude, 
           artist_longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT TIMESTAMP 'epoch' + ts / 1000 * INTERVAL '1 second' AS start_time,
           EXTRACT(HOUR FROM start_time),
           EXTRACT(DAY FROM start_time),
           EXTRACT(WEEK FROM start_time),
           EXTRACT(MONTH FROM start_time),
           EXTRACT(YEAR FROM start_time),
           EXTRACT(DOW FROM start_time)
    FROM staging_events
    WHERE ts IS NOT NULL;
""")

# QUERY LISTS

create_table_queries = [
    staging_events_table_create, 
    staging_songs_table_create, 
    user_table_create, 
    artist_table_create, 
    song_table_create, 
    time_table_create, 
    songplay_table_create
    ]
drop_table_queries = [
    staging_events_table_drop, 
    staging_songs_table_drop, 
    songplay_table_drop, 
    user_table_drop, 
    song_table_drop, 
    artist_table_drop, 
    time_table_drop
    ]
copy_table_queries = [
    staging_events_copy, 
    staging_songs_copy
    ]
insert_table_queries = [
    user_table_insert, 
    song_table_insert, 
    artist_table_insert, 
    time_table_insert, 
    songplay_table_insert, 
    ]
