"""
Import required python packages and sql queries
"""
import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Define function to load staging tables
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

def insert_tables(cur, conn):
    """
    Define function to insert row data into analytics tables
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

        
def main():
    """
    Read the config file using 'configparser'
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    """
    Connect to database using 'psycopg2'
    """
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    """
    Call the fuctions defined above
    """
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    """
    Close connection to database
    """
    conn.close()


if __name__ == "__main__":
    main()