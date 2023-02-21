# Data process - Sparkfy

## Purpose and goals
The purpose of this project is to develop a dataset to analyze the user activity on the new music streaming app. 

The mainly goal is to facilitate the analyze by creating a dataset to better aproach the data with the need of a manually extraction of  directories of JSON logs, but instead with Postgres database which should be design to optimize queries for that purpose. 

## Running the Python scripts
To do so, the Python scripts should be ran on the following sequence, first the create_tables.py since the sql_queries.py is ready to be used. 

```python
## On the create_tables.py

## Function to create the tables, going through the create_table_querie creating the tables to each table variable
def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
        
## Where the crate_table function are called, after configurating cur and cunn with the create_database() function and drop possible tables on the database with the drop_tables function.
        
def main():
    """
    - Drops (if exists) and Creates the sparkify database. 
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()

```      
        
Then the etl.py should be the next Python script to be ran.

```python

## Main function that execute process_data on the dataset avalible after configurating the coon and cur parameters.

def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()

```


## Files on the repository
The repository are compose with the Python scripts, the Jupyter notebooks files, a .md file and a folder that consist on the JSON logs.

## Database schema design and ETL pipeline
The tables are divide on songplay_table, user_table, song_table, artist_tablea and time_table. 


Each table have it's primary key, on the songplay_table the column songplay_id is the primary key, on the user_table is the user_id, on the song_table is the song_id, on the artist_tablea is the artist_id and on the time_table is the start_time. 

The songplay_table are compose with user_id, song_id, artist_id and session_id and that's how it is related with the others tables. 

```python
## On the sql_queries.py

# Configurating the columns data type and seting the pramary key.
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
                        UNIQUE (start_time, 
                                user_id, 
                                song_id, 
                                artist_id)
                        );""")   


## Inserting what was set above on the list with the other set up tables. 
create_table_queries = [songplay_table_create,
                           user_table_create,
                           song_table_create,
                           artist_table_create,
                           time_table_create]
```


The pipeline reads the JSONs file and extructure it to a list to be filled to the database's tables.

```python

# On the etl.py seting process_song_file function to go through the files and execute the insert funciton on the table after extrating the data and extructered on the artist_data. 

def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df.loc[:,['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df.loc[:,['artist_id', 'artist_name', 
                            'artist_location','artist_latitude',
                            'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)

```    
Also converts the ms values to time stamp.

```python
def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], utc=True, unit='ms')
    
    # insert time data records
    time_data = (t.tolist(),
                 t.dt.hour.values.tolist(), 
                 t.dt.day.values.tolist(),
                 t.dt.week.values.tolist(),
                 t.dt.month.values.tolist(), 
                 t.dt.year.values.tolist(),
                 t.dt.weekday.values.tolist())
    column_labels = ('start_time','hour', 'day','week','month','year','weekday')
    time_df = pd.DataFrame(list(time_data), index = list(column_labels)).transpose()

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))
## [...]     
```