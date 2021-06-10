from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql import types as T


def create_spark_session():
    """
    This initiates a Spark session or fetches an already existing one 
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    this processes song data from s3 bucket and transforms them
    into songs and artists tables
    """
    song_data = 'song_data/*/*/*/*.json'
    song_data_path = os.path.join(input_data, song_data)
    
    # read song data file
    df_song = spark.read.json(song_data_path)
    
    # create a view for df_song
    df_song.createOrReplaceTempView("song_data")

    # extract columns to create songs table
    songs_table = spark.sql("""
                    SELECT DISTINCT
                        song_id, title, artist_id, year, duration
                    FROM song_data
                    WHERE song_id IS NOT NULL
                    """)
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy("year", "artist").mode("overwrite").parquet(output_data + "songs.parquet")

    # extract columns to create artists table
    artists_table =  spark.sql("""
                    SELECT DISTINCT
                        artist_id, 
                        artist_name AS name,
                        artist_location AS location,
                        artist_latitude AS latitude,
                        artist_longitude AS longitude
                    FROM song_data
                    WHERE artist_id IS NOT NULL
                    """)
    
    # write artists table to parquet files
    artists_table.write.mode("overwrite").parquet(output_data + "artists.parquet")


def process_log_data(spark, input_data, output_data):
    """
    This processes log data from s3 bucket and transforms them
    into users, time and songplay tables
    """
    # get filepath to log data file
    log_data = 'log-data/*.json'
    log_data_path = os.path.join(input_data, log_data)

    # read log data file
    df_log = spark.read.json(log_data_path)
    
    
    # filter by actions for song plays
    df_log = df_log.where("page = 'NextSong'")
    
    # Create a view for df_log
    df_log.createOrReplaceTempView("log_data")
    
    # extract columns for users table  
    
    users_table = spark.sql("""
                SELECT DISTINCT
                    userId AS user_id,
                    firstName AS first_name,
                    lastName AS last_name,
                    gender,
                    level
                FROM log_data
                WHERE userId IS NOT NULL
                """)
    
    # write users table to parquet files
    users_table.write.mode("overwrite").parquet(output_data + "users.parquet")

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x:( int(int(x)/ 1000)))
    df_log = df_log.withColumn("timestamp", get_timestamp(df_log.ts))
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: datetime.fromtimestamp(x), T.TimestampType())
    df_log = df_log.withColumn("date", get_datetime(df_log.timestamp))
    
    # create another view of the transformed df_log
    df_log.createOrReplaceTempView("log_data")
    
    # extract columns to create time table
    time_table = spark.sql("""
                SELECT DISTINCT
                    date AS start_time,
                    hour(date) AS hour,
                    day(date) AS day,
                    weekofyear(date) AS week,
                    month(date) AS month,
                    year(date) AS year,
                    date_format(date, "EEEE") AS weekday
                FROM log_data
                WHERE date IS NOT NULL
                """)
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy("year", "month").mode("overwrite").parquet(output_data + "time.parquet")

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = spark.sql("""
                    SELECT DISTINCT
                        monotonically_increasing_id() AS songplay_id,
                        L.date AS start_time,
                        L.userId AS user_id,
                        L.level AS level,
                        S.song_id AS song_id,
                        S.artist_id AS artist_id,
                        L.sessionId AS session_id,
                        L.location AS location,
                        L.userAgent AS user_agent,
                        month(L.date) AS month,
                        year(L.date) AS year
                    FROM song_data AS S 
                        JOIN log_data AS L 
                            ON (S.artist_name = L.artist) AND (S.title = L.song) AND (S.duration = L.length)
                    """)

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy("year", "month").mode("overwrite").parquet(output_data + "songplays.parquet")


def main():
    """
    This calls all of the earlier defined functions above and reads in the input
    and output path.
    """
    spark = create_spark_session()
    #input_data = "s3a://udacity-dend/"
    #output_data = "s3a://kokobucket/"
    input_data = config.get('IO', 'INPUT_DATA')
    output_data = config.get('IO', 'OUTPUT_DATA')
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
