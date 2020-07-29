import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import TimestampType
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql import functions as F

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    # get filepath to song data file
    song_data = os.path.join(input_data, 'song_data/*/*/*/*.json')
    
    # read song data file
    schema = """
        `num_songs` LONG, 
        `artist_id` STRING, 
        `artist_latitude` DOUBLE,
        `artist_longitude` DOUBLE, 
        `artist_location` STRING, 
        `artist_name` STRING,
        `song_id` STRING, 
        `title` STRING, 
        `duration` DOUBLE, 
        `year` LONG
        """
    df = (
        spark.read.json(song_data, schema=schema)
        .dropDuplicates().cache()
        )

    # extract columns to create songs table
    songs_table = (
        df.select('song_id', 'title', 'artist_id', 'year', 'duration')
        .distinct()
        )
    
    # write songs table to parquet files partitioned by year and artist
    (songs_table
        .write.partitionBy('year', 'artist_id')
        .parquet(os.path.join(output_data, 'songs/'), mode='overwrite')
        )

    # extract columns to create artists table
    artists_table = (
        df.select(
            df.artist_id, 
            df.artist_name.alias('name'), 
            df.artist_location.alias('location'), 
            df.artist_latitude.alias('latitude'), 
            df.artist_longitude.alias('longitude')
            ).distinct()
        )
    
    # write artists table to parquet files
    (artists_table
         .write.parquet(
             os.path.join(output_data, 'artists/'), 
             mode='overwrite'
             )
        )


def process_log_data(spark, input_data, output_data):
    # get filepath to log data file
    log_data = os.path.join(input_data, 'log_data/*.json')

    # read log data file
    schema = """
        `artist` STRING,
        `auth` STRING,
        `firstName` STRING,
        `gender` STRING,
        `itemInSession` LONG,
        `lastName` STRING,
        `length` DOUBLE,
        `level` STRING,
        `location` STRING,
        `method` STRING,
        `page` STRING,
        `registration` DOUBLE,
        `sessionId` LONG,
        `song` STRING,
        `status` LONG,
        `ts` LONG,
        `userAgent` STRING,
        `userId` STRING"""
    df = (
        spark.read.json(log_data, schema=schema)
        .dropDuplicates()
        )
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong').cache()
    
    # extract columns for users table
    users_table = (
        df.select(
            df.userId.alias('user_id'),
            df.firstName.alias('first_name'),
            df.lastName.alias('last_name'),
            df.gender,
            df.level
            )
        .distinct()
        )
    
    # write users table to parquet files
    (users_table
        .write.parquet(
            os.path.join(output_data, 'users/'), 
            mode='overwrite'
            )
        )

    # create timestamp column from original timestamp column
    get_timestamp = udf(
        lambda x: datetime.fromtimestamp(x / 1000.0), 
        TimestampType()
        )
    df = df.withColumn('start_time', get_timestamp('ts'))
    df = (
        df.withColumn('hour', hour('start_time'))
        .withColumn('day', dayofmonth('start_time'))
        .withColumn('week', weekofyear('start_time'))
        .withColumn('month', month('start_time'))
        .withColumn('year', year('start_time'))
        .withColumn('weekday', date_format('start_time', 'E'))
        )
    
    # extract columns to create time table
    time_table = (
        df.select(
            'start_time','hour','day',
            'week','month','year','weekday'
            )
        .distinct()
        )
    
    # write time table to parquet files partitioned by year and month
    (time_table
        .write.partitionBy('year', 'month')
        .parquet(os.path.join(output_data, 'time/'), mode='overwrite')
        )

    # read in song data to use for songplays table
    song_df = spark.read.parquet(os.path.join(output_data, 'songs/'))

    # extract columns from joined song and log datasets to create songplays table
    songplays_table = df.join(song_df, df.song == song_df.title, 'left').drop(song_df.year)
    songplays_table = songplays_table.withColumn('songplay_id', F.monotonically_increasing_id())
    songplays_table = songplays_table.selectExpr(
        'songplay_id', 'start_time', 'userId as user_id', 
        'level', 'song_id', 'artist_id', 'sessionId as session_id', 
        'location', 'userAgent as user_agent', 'year', 'month'
        )

    # write songplays table to parquet files partitioned by year and month
    (songplays_table
        .write.partitionBy('year', 'month')
        .parquet(os.path.join(output_data, 'songplays/'), mode='overwrite')
        )


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3://"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
