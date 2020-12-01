from db_handler import DbHandler
#import proxy_parser


db_handler = DbHandler()
db_handler.connect()
db_handler.create_tables()
db_handler.close()








