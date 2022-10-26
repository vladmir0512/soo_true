from models import *
import traceback

def create_tables(): # возвращает True или False

    models = [Post, Person, Comment, Toxic_Comment, Toxic_Post] # Позже добавить Plot
    try:
        db.create_tables(models)
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
        return False

    return True

def addPost(id_post, post_text, post_ref, time_check_first, time_last_comment,post_date):  # возвращает True или False
    try:
        Post.insert(id_post=id_post,
                    post_text=post_text,
                    post_ref=post_ref,
                    time_check_first=time_check_first,
                    time_last_comment=time_last_comment,
                    post_date=post_date
                    ).execute()

        print(f"Add post id {id_post} in the \"{Post._meta.table_name}\" table\n")
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
        return False
    return True

def addPerson(id_person,first_name,second_name,city,
                country,education,occupation,family,
                birthday,alcohol,smoke,political,interests):  # возвращает True или False
    try:
        Person.insert(  
                        id_person=id_person, # логин (идентификатор ВК)
                        first_name=first_name,
                        second_name=second_name,
                        city=city,
                        country=country,
                        education=education,
                        occupation=occupation,
                        family=family,
                        birthday=birthday,
                        alcohol=alcohol,
                        smoke=smoke,
                        political=political,
                        interests=interests
                    ).execute()

        print(f"Add person id {id_person} in the \"{Person._meta.table_name}\" table")
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
        return False
    return True

def addComment(id_comment,id_post,id_person,comment,post_date):
    try:
        Comment.insert(id_comment=id_comment,
                    id_post=id_post,
                    id_person=id_person,
                    comment=comment,
                    post_date=post_date
                    ).execute()

        print(f"Add comment id {id_comment} in the \"{Comment._meta.table_name}\" table")
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
        return False
    return True

def addToxicComment(id_comment,toxic):
    try:
        Toxic_Comment.insert(
                            id_comment=id_comment,
                            toxic=toxic,
                    ).execute()

        print(f"Add toxic comment id {id_comment} in the \"{Toxic_Comment._meta.table_name}\" table")
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
        return False
    return True

def addToxicPost(id_post,toxic,count):
    try:
        Toxic_Post.insert(
                        id_post=id_post,
                        toxic=toxic,
                        count=count
                    ).execute()

        print(f"Add toxic comment id {id_post} in the \"{Toxic_Post._meta.table_name}\" table")
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
        return False
    return True

def getOldCheckPostId():   # возвращает искомый id или False или None
    try:
        oldCheck = Post.select().order_by(Post.time_check_first).get()
        if not oldCheck.exists():
            print(f"The id {oldCheck} in the \"{Post._meta.table_name}\" table does not exist.")            
            return False
        print(f"Select old check post id {oldCheck} in the \"{Post._meta.table_name}\" table")
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
        return None
    return oldCheck

def getLastPostId():     # возвращает искомый id или False или None
    try:
        last = Post.select().order_by(Post.time_last_comment.desc()).get()
        if not last.exists():
            print(f"The id {last} in the \"{Post._meta.table_name}\" table does not exist.")            
            return False
        print(f"Select last post id {last} in the \"{Post._meta.table_name}\" table")
    except Exception:
            print('Ошибка:\n', traceback.format_exc())
            return False
    return last

def getSamePostId(id_post): # возвращает True или False
    try:
        same = Post.select().where(Post.id_post == id_post).get()
        print(f"The same post id {same} exists in \"{Post._meta.table_name}\" table")
    except Exception as e:
        if str(type(e)) == "<class 'models.PostDoesNotExist'>":
            print("Same post does not exist in database.")
        else:
            print('Ошибка:\n', traceback.format_exc())
                
        
        #print('Ошибка:\n', traceback.format_exc())
        return False
    return True
    

def getSameCommentId(id_comment): # возвращает True или False
    try:
        same = Comment.select().where(Comment.id_comment == id_comment).order_by(Comment.time_last_comment.desc()).get()
        print(f"Finde the same comment id {same} in \"{Post._meta.table_name}\" table")
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
        return False
    return True

def changeFlag(id_post, flag):
    if flag in [1,"T","True"]:
        flag = True
    elif flag in [0,"F", "False"]:
        flag = False
    else:
        print("Unexpected flag value.")
        return False
    try:
        #same = Post.select().where(Post.id_post == id_post).order_by(Post.time_last_comment.desc()).get()
        Toxic_Post.update({Toxic_Post.count: False}).where(Toxic_Post.id_post == id_post).execute() 

        print(f"Flag count is changed to {flag} in \"{Toxic_Post._meta.table_name}\" table")
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
        return False
    return True

if __name__ == '__main__':   
    create_tables()
    getLastPostId()
    getOldCheckPostId()

    # Job.select(fn.MAX(Job.job_num)).scalar()
    # addPost("23","Блаблабла22","https://vk.com/vladmir05122",14,184,100) #addPost() работает
    # addPost("123","бла22","https://vk.com/vladmir05122",4,4,1000)
    # addPost("444","бла22","https://vk.com/vladmir05122",1,1,10000)
   
    
    
    # getLastPostId()  #getLastPostId() работает
    # last = Post.select().order_by(Post.time_last_comment.desc()).get()
    # print(last)
    # addPerson("1","Иван","Иванов", "Москва","Россия", "МГУ", "...", "Женат", "01.01.1993", "Негативно", "Нейтрально", "Нейтралитет", "Играю на гитаре")
    # print(getSamePostId("1"))
    # print(getSamePostId("123")
    # getSamePostId("444")