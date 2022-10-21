
from models import *

if __name__ == '__main__':
    try:
        Post.create_table()
    except InternalError as px:
        print(str(px))

    try:
      
        Person.create_table()
    except InternalError as px:
        print(str(px))

    try:
       
        Comment.create_table()
    except InternalError as px:
        print(str(px))

    try:
       
        Toxic_Comment.create_table()
    except InternalError as px:
        print(str(px))

    try:
        
        
        Toxic_Post.create_table()
    except InternalError as px:
        print(str(px))    
    
    '''
    try:
        db.connect()
        Plot.create_table()
    except peewee.InternalError as px:
        print(str(px))
    '''