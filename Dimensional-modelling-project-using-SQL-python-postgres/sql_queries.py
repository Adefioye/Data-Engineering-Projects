# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = """
    CREATE TABLE songplays (
        songplay_id SERIAL,
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
    
"""

# songplay_id, start_time, user_id, level, song_id, artist_id,
# session_id, location, user_agent

user_table_create = """
    CREATE TABLE users (
        user_id int,
        first_name varchar,
        last_name varchar,
        gender varchar,
        level varchar,
        CONSTRAINT PK_users PRIMARY KEY(user_id)
    );
"""

# user_id, first_name, last_name, gender, level

song_table_create = """
    CREATE TABLE songs (
        song_id varchar,
        title varchar,
        artist_id varchar,
        year int,
        duration numeric,
        CONSTRAINT PK_songs PRIMARY KEY(song_id)
    );
"""

# song_id, title, artist_id, year, duration

artist_table_create = """
    CREATE TABLE artists (
        artist_id varchar,
        name varchar,
        location varchar,
        latitude numeric,
        longitude numeric,
        CONSTRAINT PK_artists PRIMARY KEY(artist_id)
    );
"""

# artist_id, name, location, latitude, longitude

time_table_create = """
    CREATE TABLE time (
        start_time timestamp,
        hour int,
        day int,
        week int,
        month int,
        year int,
        weekday varchar,
        CONSTRAINT PK_time PRIMARY KEY(start_time)
    );    
"""

# start_time, hour, day, week, month, year, weekday

# INSERT RECORDS

songplay_table_insert = """
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT 
    DO NOTHING
"""

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT 
    DO NOTHING;
""")

song_table_insert = """
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT 
    DO NOTHING;
"""

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT 
    DO NOTHING;
""")

# start_time, hour, day, week, month, year, weekday

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT 
    DO NOTHING;
""")

# FIND SONGS

song_select = """
    SELECT S.song_id, A.artist_id
    FROM songs AS S
        JOIN artists AS A ON S.artist_id = A.artist_id
    WHERE S.title = %s AND A.name = %s AND S.duration = %s;
"""

# QUERY LISTS

# It is important to create songplays table last because it references columns in other tables

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [user_table_drop, song_table_drop, artist_table_drop, time_table_drop, songplay_table_drop]