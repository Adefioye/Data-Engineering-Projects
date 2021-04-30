"""
Import required python packages and sql queries
"""
import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drop all tables
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Create all tables
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Read the config file
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    """
    Connect to database and creates cursor object
    """
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    """
    Call the functions above
    """
    drop_tables(cur, conn)
    create_tables(cur, conn)

    """
    Close connection to database
    """
    conn.close()


if __name__ == "__main__":
    main()