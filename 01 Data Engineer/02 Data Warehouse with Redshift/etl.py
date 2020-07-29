import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Description: Load song and log data into staging tables
    
    Arguments:
        cur: the cursor object. 
        conn: the connection object. 
    Returns:
        None
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Description: Insert records from staging tables 
                 into fact and dimension tables
    
    Arguments:
        cur: the cursor object. 
        conn: the connection object. 
    Returns:
        None
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Description: Read config parameters from dwh.cfg
                 Setup connection and get connection cursur
                 Perform load staging tables
                 Perofrm load fact and dimension tables
                 Close connection to db
    
    Arguments:
        None
    Returns:
        None
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()