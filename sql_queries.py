# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS song;"
artist_table_drop = "DROP TABLE IF EXISTS artist;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = (""" CREATE TABLE IF NOT EXISTS songplays
                        (songplay_id SERIAL PRIMARY KEY, 
                        start_time timestamp NOT NULL,
                        user_id INT NOT NULL, 
                        level VARCHAR, 
                        song_id VARCHAR, 
                        artist_id VARCHAR, 
                        session_id INT, 
                        location VARCHAR, 
                        user_agent VARCHAR,    
    UNIQUE (start_time, user_id, song_id, artist_id));""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users \
                    (user_id bigint PRIMARY KEY, \
                    first_name varchar, \
                    last_name varchar, \
                    gender varchar, \
                    level varchar);""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS song\
                    (song_id varchar PRIMARY KEY, \
                     title varchar NOT NULL, \
                     artist_id varchar NOT NULL, \
                     year int, \
                     duration numeric NOT NULL);""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artist \
                      (artist_id varchar PRIMARY KEY, \
                      name varchar NOT NULL, \
                      location varchar, \
                      latitude double precision, \
                      longitude double precision);""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time \
                    (start_time timestamp PRIMARY KEY, \
                     hour int, \
                     day int, \
                     week int, \
                     month int, \
                     year int, \
                     weekday varchar);""")

# INSERT RECORDS

songplay_table_insert = (""" INSERT INTO songplays (
                                                    start_time, \
                                                    user_id, \
                                                    level, \
                                                    song_id, \
                                                    artist_id, \
                                                    session_id, \
                                                    location, \
                                                    user_agent)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (start_time, user_id, song_id, artist_id) DO UPDATE
                        SET start_time = %s, 
                        user_id = %s,
                        level = %s, 
                        song_id = %s, 
                        artist_id = %s, 
                        session_id = %s, 
                        location = %s, 
                        user_agent = %s;
                        """);

user_table_insert = ("""INSERT INTO users (
                                            user_id, \
                                            first_name, \
                                            last_name, \
                                            gender, \
                                            level)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (user_id)
                    DO UPDATE SET level = EXCLUDED.level;
""")

song_table_insert = ("""INSERT INTO song (
                                            song_id, \
                                            title, \
                                            artist_id, \
                                            year, \
                                            duration)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (song_id) DO NOTHING;
""")

artist_table_insert = ("""INSERT INTO artist (
                                                artist_id, \
                                                name, \
                                                location, \
                                                latitude, \
                                                longitude)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (artist_id) DO NOTHING;
""")


time_table_insert = ("""INSERT INTO time (
            start_time,hour,day,week,month,year,weekday)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
""")

# FIND SONGS

song_select = ("""SELECT song_id, song.artist_id
                FROM song 
                JOIN artist ON song.artist_id=artist.artist_id
                WHERE title=%s AND name=%s AND duration=%s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]