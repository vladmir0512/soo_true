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

a = db.connect()
print(a)




#Create models
class BaseModel(peewee.Model):

	class Meta:
		database = db

class Post(BaseModel):
	'''
	id_post = Charfield(max_length=18)
	post_text = CharField()

	- ссылка на пост
	- время проверки комментариев
	- время последнего комментарияесли нет комментариев в течении 
	(48 часов, то проверять раз в неделю, раз …)

	'''

class Person(BaseModel):
	'''
	- id
	- информация
	- логин (идентификатор ВК)
	'''

class Comment(BaseModel):
	'''
	- id_ВК_поста
	- идентификатор ВК человека
	- комментарий
	- дата/время
	'''

class Toxic_Comment(BaseModel):
	'''
	- id комментария
	- токсичность
	'''

class Toxic_Post(BaseModel):
	'''
	- id_поста
	- токсичность
	- пересчитать (флаг, Boolean)
	'''

class Plot(BaseModel):
	'''
	- тип (Hscore) – json хранить все схожие id постов, Array.
	- мешок слов
	- вектор … цифрой
	'''
