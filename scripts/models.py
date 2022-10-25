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

	id_post = pw.CharField(max_length=18, unique=True, primary_key=True)
	post_text = pw.CharField()
	post_ref = pw.CharField()
	time_check_first = pw.IntegerField()
	time_last_comment = pw.IntegerField()
	post_date = pw.IntegerField()

class Person(BaseModel):

	class Meta:
		db_table = 'persons'

	id_person = pw.CharField(unique=True, primary_key=True) # логин (идентификатор ВК)
	first_name = pw.CharField()
	second_name = pw.CharField()
	city = pw.CharField()
	country = pw.CharField()
	education = pw.CharField()
	occupation = pw.CharField()
	family = pw.CharField()
	birthday = pw.CharField()
	alcohol = pw.CharField()
	smoke = pw.CharField()
	political = pw.CharField()
	interests = pw.CharField()


class Comment(BaseModel):

	class Meta:
		db_table = 'comments'

	id_comment = pw.CharField(unique=True, primary_key=True) 
	id_post = pw.ForeignKeyField(Post)
	id_person = pw.ForeignKeyField(Person)
	comment = pw.CharField()
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
