from peewee import *
from vars import *
import os

#Connect to postgres db
user = 'postgres'
password = os.getenv("PG_PASSWORD")
db_name = 'postgres'
host = '0.0.0.0' 
port = 5433
db = PostgresqlDatabase(
			db_name,
			autocommit=True,
			autorollback=True,
			user=user,
			password=password,
            host=host,
			port=port
)


#Create models
class BaseModel(Model):

	class Meta:
		database = db


class Post(BaseModel):

	class Meta:
		db_table = 'posts'

	id_post = CharField(max_length=18, unique=True, primary_key=True)
	post_text = CharField()
	post_ref = CharField()
	time_check_first = IntegerField()
	time_last_comment = IntegerField()


class Person(BaseModel):

	class Meta:
		db_table = 'persons'

	id_person = CharField(unique=True, primary_key=True) # логин (идентификатор ВК)
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

	class Meta:
		db_table = 'comments'

	id_comment = CharField(unique=True, primary_key=True) 
	id_post = ForeignKeyField(Post)
	id_person = ForeignKeyField(Person)
	comment = CharField()
	post_date = IntegerField()
	

class Toxic_Comment(BaseModel):

	class Meta:
		db_table = 'toxic_comments'

	id_comment = ForeignKeyField(Comment,unique=True, primary_key=True)
	toxic = FloatField()
	

class Toxic_Post(BaseModel):
	
	class Meta:
		db_table = 'toxic_posts'

	id_post = ForeignKeyField(Post,unique=True, primary_key=True)
	toxic = DoubleField()
	count = BooleanField()


	 
# class Plot(BaseModel):
# 	plotType =HStoreField
# 	- тип (Hscore) – json хранить все схожие id постов, Array.
# 	- мешок слов
# 	- вектор … цифрой
# 	'''
