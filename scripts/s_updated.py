import time

import vk_api

import operations as orm
import traceback
import os
import vars

from datetime import datetime
from toxic import text2toxicity



def get_posts(group_id):
    
    i=0
    exit=False
    
    if group_id == '26284064' and i == 0:
        i = 1
    
    while exit==False:
        wall = session.method('wall.get', {"owner_id": '-' + group_id,"count":1,"offset":i})
        post_id = group_id + '_' + str(wall['items'][0]['id'])

        if i > post_lim or orm.getSamePostId(post_id):
            break 
        
        postlink = ("https://vk.com/public" + str(group_id) + "?w=wall" + str('-'+group_id) + "_" + str(wall['items'][0]['id']))
        time=0  
        orm.addPost(
            post_id,
            wall['items'][0]['text'],
            postlink,
            time, 
            0, 
            wall['items'][0]['date'])
        i+=1



def get_comments(group_id):
    global family, alcohol, smoke, political
    post_id_full=orm.getOldCheckPostId()
    post_id=str(post_id_full.split("_")[1])
    comments = session.method('wall.getComments', {"owner_id": "-"+group_id, "post_id": post_id, "extended": 1})
    for comment in (comments["items"]):
        try:
            from_id = comment["from_id"]
            
            if from_id <= 0:
                continue
            
            comment_id = str(group_id) + "_" + str(comment['id'])
            user = session.method("users.get", {"user_ids": from_id, "fields": "city,country,education,occupation,bdate,personal,relation,interests"})
            
            
            
            try:   
                samePerson = orm.getSamePersonId(from_id)
            except Exception:
                print('Ошибка:\n', traceback.format_exc())
            
            if not samePerson:#Проверка на то, есть ли этот человек в бд, и если его нет, выполняем парсинг его данных и их добавление:
                name = user[-1]['first_name']
                lastname = user[-1]['last_name']
                
                try:
                    if "city" in user[-1]:
                        city = user[-1]["city"]
                        city = city["title"]
                    else:
                        city = '0'
                        
                    
                    
                except Exception:
                    print('Ошибка:\n', traceback.format_exc())
                    
                    
                try:
                    
                    if "country" in user[-1]:
                        country = user[-1]["country"]
                        country = country["title"]
                        
                    else:
                        country = '0'
                    
                        
                    
                except Exception:
                    print('Ошибка:\n', traceback.format_exc())
                
                    
                    
                try:
                    if "education" in user[-1]:
                        education = user[-1]["education"]
                        education = education["university_name"]
                        
                    else:
                        education = '0'
                        
                    
                except Exception:
                    print('Ошибка:\n', traceback.format_exc())
                    
                    
                    
                try:
        
                    if "occupation" in user[-1]:
                        occupation = user[-1]["occupation"]
                        occupation = occupation["name"]
                        
                    else:
                        occupation = '0'
                        
                     
                except Exception:
                    print('Ошибка:\n', traceback.format_exc())
                    
                    
                    
                
                try:
                  
                    if "relation" in user[-1]:
                        familyInt = user[-1]["relation"]
                
                        if familyInt == 1:
                            family = "не женат/не замужем"
                        elif familyInt == 2:
                            family = "есть друг/есть подруга"
                        elif familyInt == 3:
                            family = "помолвлен/помолвлена"
                        elif familyInt == 4:
                            family = "женат/замужем"
                        elif familyInt == 5:
                            family = "всё сложно"
                        elif familyInt == 6:
                            family = "в активном поиске"
                        elif familyInt == 7:
                            family = "влюблён/влюблена"
                        elif familyInt == 8:
                            family = "в гражданском браке"
                    else:
                        family = "0"
                        
                except Exception:
                    print('Ошибка:\n', traceback.format_exc())
                    
                    
                    
                try:
                    birthday = user[-1]['bdate']
                    if not birthday:
                        birthday = '0'
                except Exception:
                    print('Ошибка:\n', traceback.format_exc())
                    
                
                
                
                try:
                    
                    if "personal" in user[-1] and "alcohol"  in user[-1]['personal']:
                        alcohol_int = user[-1]['personal']["alcohol"]
                        
                        if alcohol_int == 1:
                            alcohol = "резко негативное"
                        elif alcohol_int == 2:
                            alcohol = "негативное"
                        elif alcohol_int == 3:
                            alcohol = "компромиссное"
                        elif alcohol_int == 4:
                            alcohol = "нейтральное"
                        elif alcohol_int == 5:
                            alcohol = "положительное"
                    else:
                        alcohol = "0"
                except Exception:
                    print('Ошибка:\n', traceback.format_exc())
                    
                    
                    
                try:
                    
                    if "personal" in user[-1] and "smoking" in user[-1]['personal']:
                        smoke_int = user[-1]['personal']["smoking"]

                        if smoke_int == 1:
                            smoke = "резко негативное"
                        elif smoke_int == 2:
                            smoke = "негативное"
                        elif smoke_int == 3:
                            smoke = "компромиссное"
                        elif smoke_int == 4:
                            smoke = "нейтральное"
                        elif smoke_int == 5:
                            smoke = "положительное"
                    else:
                        smoke = "0"
                except Exception:
                    print('Ошибка:\n', traceback.format_exc())
                    
                    
                    
                try:
                    if "personal" in user[-1] and "political" in user[-1]['personal']:
                        political_int = user[-1]['personal']["political"]

                        if political_int == 1:
                            political = "коммунистические"
                        elif political_int == 2:
                            political = "социалистические"
                        elif political_int == 3:
                            political = "умеренные"
                        elif political_int == 4:
                            political = "либеральные"
                        elif political_int == 5:
                            political = "консервативные."
                        elif political_int == 6:
                            political = "монархические"
                        elif political_int == 7:
                            political = "ультраконсервативные"
                        elif political_int == 8:
                            political = "индифферентные"
                        elif political_int == 9:
                            political = "либертарианские"
                    else:
                        political = "0"
                except Exception:
                    print('Ошибка:\n', traceback.format_exc())
                    
                    
                try:
                    if "interests" in user[-1]:
                        interests = user[-1]['interests']
                    else:
                        interests = "0"
                except Exception:
                    print('Ошибка:\n', traceback.format_exc())
                
                    
                    
                # Добавляем в бд информацию по человеку
                orm.addPerson(from_id, name, lastname, city,country, education, occupation, family,birthday, alcohol, smoke, political, interests)
            
                
              
                    
            try:   
                sameComment = orm.getSameCommentId(from_id)
            except Exception:
                print('Ошибка:\n', traceback.format_exc())
            
            if sameComment:
                continue
                
            try:   
                orm.addComment(comment_id, post_id_full, from_id, comment["text"], comment["date"])
            except Exception:
                print('Ошибка:\n', traceback.format_exc())
            
           
            # try:
            #     orm.changeFlag()
            # except Exception:
            #     print('Ошибка:\n', traceback.format_exc())

            
        except Exception:
            print('Ошибка:\n', traceback.format_exc())

def toxic():
    try:
        comments_and_ids = orm.toxicGetComment() #получить комменты, которые есть в comments, но которых нет в toxic_comments
        a = []
        id_and_toxic = tuple()
        for comment in comments_and_ids:  
            a.append(comment.comment)

        toxic_list = text2toxicity(a)
        
        id_and_toxic = (comments_and_ids), (toxic_list)
        
        for toxic_comment in toxic_list:
            number = list(toxic_list).index(toxic_comment)
            id_comment = id_and_toxic[0][number]
            toxic = id_and_toxic[1][number]
            orm.addToxicComment(id_comment, toxic)
    except Exception as e:
            if str(type(e)) == "<class 'IndexError'>":
                    print("Toxicity already calculated.")
                    return False
            else:
                print('Ошибка:\n', traceback.format_exc())
                return False


if __name__== '__main__':
    orm.create_tables()
    toxic()
    # new_list = [0, 3, 25, 523]
    # for el in new_list:
    #     print(new_list.index(el))
    # group_id = '26284064'
    # post_lim = int(os.getenv("POSTLIM"))
    # token = os.getenv("TOKEN")
    # session = vk_api.VkApi(token=token)
    # vk = session.get_api()

    # print(f'Start {datetime.now()}\n')
    # orm.create_tables()
    # get_posts(group_id)
    # get_comments(group_id)
    
    # print(f"\nStopped {datetime.now()}")

