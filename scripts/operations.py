from models import *


if __name__ == '__main__':   
    models = [Post, Person, Comment, Toxic_Comment, Toxic_Post] # Позже добавить Plot
    try:
        db.create_tables(models)
    except InternalError:
        print("Tables not created!")


  
  