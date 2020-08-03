# DROP TABLES

immigrations_table_drop = "DROP TABLE IF EXISTS immigrations;"
temperature_table_drop = "DROP TABLE IF EXISTS temperature;"
demographics_table_drop = "DROP TABLE IF EXISTS demographics;"
airports_table_drop = "DROP TABLE IF EXISTS airports;"

# CREATE TABLES

immigrations_table_create = ("""
     CREATE TABLE IF NOT EXISTS immigrations (
         cicid VARCHAR PRIMARY KEY,
         cit VARCHAR,
         res VARCHAR,
         biryear SMALLINT,
         gender VARCHAR,
         iata VARCHAR,
         arrdate BIGINT,
         mode VARCHAR,
         city VARCHAR,
         state VARCHAR,
         depdate BIGINT,
         visa VARCHAR,
         visatype VARCHAR,
         admnum DOUBLE PRECISION,
         airline VARCHAR,
         fltno VARCHAR,
         count SMALLINT
    );
""")


temperature_table_create = ("""
    CREATE TABLE IF NOT EXISTS temperature (
        city VARCHAR PRIMARY KEY,
        average_temperature REAL,
        latitude VARCHAR,
        longitude VARCHAR
    );
""")

demographics_table_create = ("""
    CREATE TABLE IF NOT EXISTS demographics (
        city VARCHAR,
        state VARCHAR,
        median_age REAL,
        male_population INTEGER,
        female_population INTEGER,
        total_population INTEGER,
        number_of_veterans INTEGER,
        number_of_foreign_born INTEGER,
        average_household_size REAL,
        state_code VARCHAR,
        race VARCHAR,
        count INTEGER,
        PRIMARY KEY (city, state, race)
    );
""")

airports_table_create = ("""
    CREATE TABLE IF NOT EXISTS airports (
        ident VARCHAR PRIMARY KEY,
        type VARCHAR,
        name VARCHAR,
        elevation_ft REAL,
        iso_country VARCHAR,
        iso_region VARCHAR,
        municipality VARCHAR,
        gps_code VARCHAR,
        iata VARCHAR
    );
""")

# INSERT RECORDS

immigrations_table_insert = ("""
    INSERT INTO immigrations
    VALUES (
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s
    )
    ON CONFLICT (cicid)
        DO NOTHING;
""")

temperature_table_insert = ("""
    INSERT INTO temperature
    VALUES (
        %s, %s, %s, %s
    )
    ON CONFLICT (city)
        DO NOTHING;
""")

demographics_table_insert = ("""
    INSERT INTO demographics
    VALUES (
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s
    )
    ON CONFLICT (city, state, race)
        DO NOTHING;
""")

airports_table_insert = ("""
    INSERT INTO airports
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    ON CONFLICT (ident)
        DO NOTHING;
""")

# QUERY LISTS

drop_table_queries = [
    immigrations_table_drop, 
    temperature_table_drop, 
    demographics_table_drop,
    airports_table_drop
]

create_table_queries = [
    immigrations_table_create, 
    temperature_table_create, 
    demographics_table_create,
    airports_table_create
]

insert_table_queries = [
    immigrations_table_insert, 
    temperature_table_insert, 
    demographics_table_insert,
    airports_table_insert
]