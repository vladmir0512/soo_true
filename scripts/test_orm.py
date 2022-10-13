from peewee import *
import os

user = 'postgres'
password = os.getenv("PG_PASSWORD")
db_name = 'postgres'
 
db = PostgresqlDatabase(
			 db_name,
			 user=user,
			 password=password,
                         host='0.0.0.0',
			 port=5433
)


