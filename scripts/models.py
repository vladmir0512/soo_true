from peewee import *
from dotenv import load_dotenv

import os
import vars

#Connect to postgres db
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

# a = db.connect()
# print(a)




#Create models
class BaseModel(Model):

	class Meta:
		database = db


class Post(BaseModel):
	id_post = CharField(max_length=18)
	post_text = CharField()
	post_ref = CharField()
	time_check_first = IntegerField()
	time_check_last =  IntegerField()


class Person(BaseModel):
	id_person = CharField() # логин (идентификатор ВК)
	first_name = CharField()
	second_name = CharField()
	city = CharField()
	country = CharField()
	education = CharField()
	occupation = CharField()
	family = CharField()
	birthday = CharField()
	alcohol = CharField()
	smoke = CharField()
	political = CharField()
	interests = CharField()


class Comment(BaseModel):
	id_comment = CharField() 
	id_post = ForeignKeyField(Post, to_field="id_post")
	id_person = ForeignKeyField(Person, to_field="id_person")
	comment = CharField()
	post_date = IntegerField()
	

class Toxic_Comment(BaseModel):
	id_comment = ForeignKeyField(Comment, to_field="id_comment")
	toxic = FloatField()
	

class Toxic_Post(BaseModel):
	id_post = ForeignKeyField(Post, to_field="id_post")
	toxic = FloatField()
	count = BooleanField()



# class Plot(BaseModel):
# 	plotType = hscore
# 	- тип (Hscore) – json хранить все схожие id постов, Array.
# 	- мешок слов
# 	- вектор … цифрой
# 	'''
