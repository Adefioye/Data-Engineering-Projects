"""
Imports package 'configparser' to read parameters from the file 'dwh.cfg'
"""
import configparser

"""
Reads the 'dwh.cfg' file
"""

config = configparser.ConfigParser()
config.read('dwh.cfg')

"""
Assigns the parameters in the config files to variables
"""
song_data = config.get("S3","SONG_DATA")
log_data = config.get("S3","LOG_DATA")
IAM_ROLE = config.get("IAM_ROLE","ARN")
JSON_PATH = config.get("S3","LOG_JSONPATH")

"""
Drops all tables
"""
staging_events_table_drop = "DROP table IF EXISTS staging_events"
staging_songs_table_drop = "DROP table IF EXISTS staging_songs"
songplay_table_drop = "DROP table IF EXISTS songplay"
user_table_drop = "DROP table IF EXISTS users"
song_table_drop = "DROP table IF EXISTS song"
artist_table_drop = "DROP table IF EXISTS artist"
time_table_drop = "DROP table IF EXISTS time"

"""
Create all tables
"""

staging_events_table_create= ("""CREATE table staging_events(
                                artist          varchar,
                                auth            varchar,
                                firstName       varchar,
                                gender          varchar,
                                itemInsession   integer,
                                lastName        varchar,
                                length          float,
                                level           varchar,
                                location        varchar,
                                method          varchar,
                                page            varchar,
                                registration    float,
                                sessionId       integer,
                                song            varchar,
                                status          integer,
                                ts              bigint,
                                userAgent       varchar,
                                userId          integer
                                )
""")

staging_songs_table_create = ("""CREATE table staging_songs(
                                num_songs         integer,
                                artist_id         varchar,
                                artist_latitude   float,
                                artist_longitude  float,
                                artist_location   varchar,
                                artist_name       varchar,
                                song_id           varchar       PRIMARY KEY,
                                title             varchar,
                                duration          float,
                                year              integer
                                )
""")


user_table_create = ("""CREATE table users(
                                user_id          integer         PRIMARY KEY    sortkey,
                                first_name       varchar,
                                last_name        varchar,
                                gender           varchar,
                                level            varchar
                                )
                                diststyle all
""")

artist_table_create = ("""CREATE table artist(
                                artist_id        varchar          PRIMARY KEY   sortkey,
                                name             varchar,
                                location         varchar,
                                latitude         float,
                                longitude        float
                                )
                                diststyle all
""")

song_table_create = ("""CREATE table song(
                                song_id          varchar          PRIMARY KEY,
                                title            varchar,
                                artist_id        varchar          sortkey,
                                year             integer,
                                duration         float,
                                CONSTRAINT fk_artist_song
                                    FOREIGN KEY(artist_id)
                                        REFERENCES artist(artist_id)
                                )
""")

time_table_create = ("""CREATE table time(
                                start_time       timestamp        PRIMARY KEY distkey,
                                hour             integer,
                                day              integer,
                                week             integer,
                                month            integer,
                                year             integer          sortkey,
                                weekday          varchar
                                )
""")

songplay_table_create = ("""CREATE table songplay(
                                songplay_id     integer          IDENTITY(0,1)     PRIMARY KEY,
                                start_time      timestamp        distkey,
                                user_id         integer          sortkey,
                                level           varchar,
                                song_id         varchar,
                                artist_id       varchar,
                                session_id      varchar,
                                location        varchar,
                                user_agent      varchar,
                                CONSTRAINT fk_time_songplay
                                    FOREIGN KEY(start_time)
                                        REFERENCES time(start_time),
                                CONSTRAINT fk_songs_songplay
                                    FOREIGN KEY(song_id)
                                        REFERENCES song(song_id),
                                CONSTRAINT fk_artist_songplay
                                    FOREIGN KEY(artist_id)
                                        REFERENCES artist(artist_id)
                                )
""")



"""
Copies data from S3 bucket to staging tables
"""
staging_songs_copy = ("""copy staging_songs
                         from '{}'
                         iam_role '{}'
                         json 'auto' region 'us-west-2';
""").format(song_data,IAM_ROLE)

staging_events_copy = ("""copy staging_events
                          from '{}'
                          iam_role '{}'
                          json '{}'region 'us-west-2';
""").format(log_data,IAM_ROLE,JSON_PATH)


"""
Inserts data from staging tables to analytics tables
"""

songplay_table_insert = ("""INSERT INTO songplay(
                                start_time,
                                user_id,
                                level,
                                song_id,
                                artist_id,
                                session_id,
                                location,
                                user_agent
                                )
                            SELECT DISTINCT
                                timestamp 'epoch' + (ts/1000) * interval '1 second',
                                userId,
                                level,
                                song_id,
                                artist_id,
                                sessionId,
                                location,
                                userAgent
                            FROM staging_events AS se
                                JOIN staging_songs AS ss
                                    ON se.artist=ss.artist_name;
""")

user_table_insert = ("""INSERT INTO users(
                                user_id,
                                first_name,
                                last_name,
                                gender,
                                level
                                )
                            SELECT DISTINCT
                                userId,
                                firstName,
                                lastName,
                                gender,
                                level
                            FROM staging_events
                            WHERE page='NextSong'
""")

song_table_insert = ("""INSERT INTO song(
                                song_id,
                                title,
                                artist_id,
                                year,
                                duration
                                )
                            SELECT DISTINCT
                                song_id,
                                title,
                                artist_id,
                                year,
                                duration
                            FROM staging_songs
""")

artist_table_insert = ("""INSERT INTO artist(
                                artist_id,
                                name,
                                location,
                                latitude,
                                longitude
                                )
                            SELECT DISTINCT
                                artist_id,
                                artist_name,
                                artist_location,
                                artist_latitude,
                                artist_longitude
                            FROM staging_songs
""")

time_table_insert = ("""INSERT INTO time(
                                start_time,
                                hour,
                                day,
                                week,
                                month,
                                year,
                                weekday
                                )
                            SELECT DISTINCT
                                timestamp 'epoch' + (ts/1000) * interval '1 second',
                                EXTRACT(h FROM TIMESTAMP 'epoch' + (ts/1000) * interval '1 second'),
                                EXTRACT(d FROM TIMESTAMP 'epoch' + (ts/1000) * interval '1 second'),
                                EXTRACT(w FROM TIMESTAMP 'epoch' + (ts/1000) * interval '1 second'),
                                EXTRACT(m FROM TIMESTAMP 'epoch' + (ts/1000) * interval '1 second'),
                                EXTRACT(y FROM TIMESTAMP 'epoch' + (ts/1000) * interval '1 second'),
                                TO_CHAR(TIMESTAMP 'epoch' + (ts/1000) * interval '1 second', 'FMDay')
                            FROM staging_events
                                
""")

"""
List of all queries as defined above
"""

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, artist_table_create, song_table_create,time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_songs_copy, staging_events_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
