# TO-DO

# This project is aimed at creating a fact table and dimension tables. 

This was done by extracting specific info from json files and loading it into a postgres database

# The following tables and their attributes were extracted from data/song_data and data/log_data

fact table:

- songplays : songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

dimension tables:

- users : user_id, first_name, last_name, gender, level
- songs : song_id, title, artist_id, year, duration
- artists : artist_id, name, location, latitude, longitude
- time : start_time, hour, day, week, month, year, weekday

