import sqlite3


class DbHandler:
    def create_tables(self):
        create_parsing_query_table = """
        CREATE TABLE IF NOT EXISTS parsing_query (
            id integer PRIMARY KEY,
            query_date text,
            url text
        )"""      
        create_proxy_table_sql = """
        CREATE TABLE IF NOT EXISTS proxy (
            id integer PRIMARY KEY,
            parsing_query_id integer FOREGIN KEY,
            ip_address text,
            port text,
            country text,
            speed text,
            type text,
            anonymity text,
            last_update_date text
        )"""
        self.cursor.execute(create_parsing_query_table)
        self.cursor.execute(create_proxy_table_sql)
        self.conn.commit()

    def connect(self):
        self.conn = sqlite3.connect('db/proxy_parser.db')
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def __init__(self):
        pass