# Background 
It is important for the startup, and indeed all businesses, to understand their consumer behaviour in order to target products and services to the right audience as well as drive product improvement. Therefore, Sparkify needs to be able to analyse its user data and derive actinable insights. The most vital data include knowing what songs, artists and genres are in high demand, the demographics of its users as well as how to use this data to effectively grow their subscriber base.
# Project Objectives
This database helps the analytics team to achieve three main goals. Firstly, it allows them to access the trove of data that has hithertho been unaccesible. Secondly, given the design schema and type of database(relational) implemented, it allows them to do a wide range of analytical queries that can help current and future questions. Lastly, this database will also help them improve the efficiecy in which they are able to respond to their user behaviours which may provide a competitve advantage to Sparkify.

# Project Dataset & Files
The  `sql_queries.py` file contains Postgres queries for dropping, creating and inserting data into the staging and analytics tables. The `create_tables.py` file contains python script for executing the sql queries for dropping and creating the tables using the psycopg2 wrapper. The `etl.py` contains scripts used to copy data into the staging tables as well as insert these data into the analytics table. The `Create_Redshift` file is used to set up the redshift cluster using IaC. Also, the `dwh.cfg` contains parameters used to create the Redshift cluster. The `test.ipynb` contains sql code for running test queries  to ascertain that the code works.


# ETL Process
Sparkify's dataset are located in an AWS S3 bucket which contains its streaming data log and song data, both in json format. A postgres redshift cluster is created and the data is copied from the S3 bucket to two staging tables in the redshift. Analytics tables are also created in the redshift and populated by inserting data from the staging tables.


# Database Schema
Database schema employed is the Star Schema with a fact Table (SongPlay) and four dimension tables (Users, Song, Artist and Time). The ETL pipeline entails reading datasets in json format containing information about the played song (Song dataset) and an event long for user streaming (Log dataset). The star schema was chosen due to the ralatively straighforward nature of the available data as well as the simplicity involved in the design.

# Running the Scripts
The `Create_Redshift.ipynb` file is run firstly to create a postgres redshift cluster and establish connection to the database. This should then be follwed by `create_tables.py` to drop tables(if exist) and create new tables. Afterwards, the `etl.py` should be run to copy data to the staging tables and further insert them into the analytics table. Finally, the `Test_File.ipynb` should then be run to execute desired queries. 

# Example Query
The following code can be used to display the most active listeners on the Sparkify platform and help tailor loyalty schemes/marketing materials to such customers.

    %%sql
    select user_id, count(user_id) as n, level
    FROM songplays
    group by user_id, level
    order by n desc
    LIMIT 10;