import peewee as pw
import os

from vars import *


#Connect to postgres db
user = 'postgres'
password = os.getenv("PG_PASSWORD")
db_name = 'postgres'
host = '0.0.0.0' 
port = 5433
db = pw.PostgresqlDatabase(

			db_name,
			autocommit=True,
			autorollback=True,
			user=user,
			password=password,
            host=host,
			port=port
)


#Create models
class BaseModel(pw.Model):

	class Meta:
		database = db


class Post(BaseModel):

	class Meta:
		db_table = 'posts'

	id_post = pw.TextField(unique=True, primary_key=True)
	post_text = pw.TextField()
	post_ref = pw.TextField()
	time_check_first = pw.IntegerField()
	time_last_comment = pw.IntegerField()
	post_date = pw.IntegerField()

class Person(BaseModel):

	class Meta:
		db_table = 'persons'

	id_person = pw.TextField(unique=True, primary_key=True) # логин (идентификатор ВК)
	first_name = pw.TextField()
	second_name = pw.TextField()
	city = pw.TextField()
	country = pw.TextField()
	education = pw.TextField()
	occupation = pw.TextField()
	family = pw.TextField()
	birthday = pw.TextField()
	alcohol = pw.TextField()
	smoke = pw.TextField()
	political = pw.TextField()
	interests = pw.TextField()


class Comment(BaseModel):

	class Meta:
		db_table = 'comments'

	id_comment = pw.TextField(unique=True, primary_key=True) 
	id_post = pw.ForeignKeyField(Post)
	id_person = pw.ForeignKeyField(Person)
	comment = pw.TextField()
	post_date = pw.ForeignKeyField(Post)
	

class Toxic_Comment(BaseModel):

	class Meta:
		db_table = 'toxic_comments'

	id_comment = pw.ForeignKeyField(Comment,unique=True, primary_key=True)
	toxic = pw.FloatField()
	

class Toxic_Post(BaseModel):
	
	class Meta:
		db_table = 'toxic_posts'

	id_post = pw.ForeignKeyField(Post,unique=True, primary_key=True)
	toxic = pw.DoubleField()
	count = pw.BooleanField()


	 
# class Plot(BaseModel):
# 	plotType =HStoreField
# 	- тип (Hscore) – json хранить все схожие id постов, Array.
# 	- мешок слов
# 	- вектор … цифрой
# 	'''
