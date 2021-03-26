# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id int,
        start_time timestamp,
        user_id int,
        level varchar,
        song_id varchar,
        artist_id varchar,
        session_id int,
        location varchar,
        user_agent varchar,
        CONSTRAINT FK_users_songplays FOREIGN KEY(user_id) REFERENCES users(user_id),
        CONSTRAINT FK_songs_songplays FOREIGN KEY(song_id) REFERENCES songs(song_id),
        CONSTRAINT FK_artists_songplays FOREIGN KEY(artist_id) REFERENCES artists(artist_id),
        CONSTRAINT FK_time_songplays FOREIGN KEY(start_time) REFERENCES time(start_time)
        
    
    
    );
    
""")

# songplay_id, start_time, user_id, level, song_id, artist_id,
# session_id, location, user_agent

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id int PRIMARY KEY,
        first_name varchar,
        last_name varchar,
        gender varchar,
        level varchar
    );
""")

# user_id, first_name, last_name, gender, level

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id varchar PRIMARY KEY,
        title varchar,
        artist_id varchar,
        year int,
        duration numeric       
    )
""")

# song_id, title, artist_id, year, duration

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id varchar PRIMARY KEY,
        name varchar,
        location varchar,
        latitude numeric,
        longitude numeric
    )
""")

# artist_id, name, location, latitude, longitude

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time timestamp PRIMARY KEY,
        hour int,
        day int,
        week int,
        month int,
        year int,
        weekday int
    )    
""")

# start_time, hour, day, week, month, year, weekday

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]