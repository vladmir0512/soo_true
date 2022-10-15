from peewee import *
from dotenv import load_dotenv

import os
import vars


user = 'postgres'
password = os.getenv("PG_PASSWORD")
db_name = 'postgres'
host = '0.0.0.0' 
port = 5433
db = PostgresqlDatabase(
			 db_name,
			 user=user,
			 password=password,
                         host=host,
			 port=port
)

connected = db.connect()

print(connected)	
