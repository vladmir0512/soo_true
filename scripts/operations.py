from models import *

def addPost(id_post, post_text, post_ref, time_check_first, time_last_comment):
    try:
        Post.insert(id_post=id_post,
                    post_text=post_text,
                    post_ref=post_ref,
                    time_check_first=time_check_first,
                    time_last_comment=time_last_comment
                    ).execute()

        print(f"Add post №{id_post} in the \"{Post._meta.table_name}\" table")
    except:
        print("The post cannot be added.")
        return False
    return True

def addPerson():
    ...

def addComment():
    ...

def addToxicComment():
    ...

def addToxicPost():
    ...

def selectLastPostId():
    try:
        last = Post.select().order_by(Post.time_last_comment.desc()).get()
        #last = Post.select(Names.ka_id).order_by(Names.ka_id.desc()).limit(1).tuples()
        print(f"Select last post id {last} in the \"{Post._meta.table_name}\" table")
    except:
        print("The id cannot be selected.")
        return False
    return last




if __name__ == '__main__':   
    models = [Post, Person, Comment, Toxic_Comment, Toxic_Post] # Позже добавить Plot
    try:
        db.create_tables(models)
    except InternalError:
        print("Tables not created!")

    addPost("23","Блаблабла22","https://vk.com/vladmir05122",14,184) #addPost() работает
    addPost("123","бла22","https://vk.com/vladmir05122",4,4)
    addPost("444","бла22","https://vk.com/vladmir05122",1,1)
    selectLastPostId()  #selectLastPostId() работает
    last = Post.select().order_by(Post.time_last_comment.desc()).get()
    print(last)
  