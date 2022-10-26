import time 
from datetime import datetime
import vk_api
import operations as orm
import os
import vars


#Функция сбора постов готова, вроде как работает. В самом итоговом варианте осталось просто поставить постоянное выполнение раз в час и добавить несколько групп
def get_posts():
    global post, group_id
    group_id = '26284064'
    i=0
    exit=False
    
    if group_id == '26284064' and i == 0:
        i = 1
    
    while exit==False:
        wall = session.method('wall.get', {"owner_id": '-' + group_id,"count":1,"offset":i})
        post_id = group_id + '_' + str(wall['items'][0]['id'])

        if i>20 or orm.getSamePostId(post_id):
            break # добавляем так, пока не дойдем до последнего, вырубаем
        
        postlink = ("https://vk.com/public" + str(group_id) + "?w=wall" + str('-'+group_id) + "_" + str(wall['items'][0]['id']))
        time=0  #Заглушка. Просто маленькое число, из-за чего функция сбора комментариев в первую очередь будет проверять именно новые добавленные посты
        orm.addPost(
            post_id,
            wall['items'][0]['text'],
            postlink,
            time,
            0,
            wall['items'][0]['date'])
        i+=1


def get_comments():
    post_id=getOldCheckPostId()
    global family
    comments = session.method('wall.getComments', {"owner_id": group_id, "post_id": post_id, "extended": 1})
    for comment in (comments["items"]):
        try:
            ExitFlag = False
            from_id = comment["from_id"]
            if from_id <= 0:
                continue
            print(comment["text"])
            user = session.method("users.get", {"user_ids": from_id, "fields": "city,country,education,occupation,bdate,personal,relation,interests"})
            name = user[-1]['first_name']
            lastname = user[-1]['last_name']
            CommentId = str(group_id) + "_" + str(comment['id'])
            #ставим проверку,если комментарий с таким ай-ди есть в базе, ставим ExitFlag True, он пропускает этот коммент
            if ExitFlag == True:
                continue
            #Проверка на то, есть ли этот человек в бд, и если его нет, выполняем парсинг его данных и их добавление:
            try:
                city = user[-1]["city"]
                city = city["title"]
            except:
                city = "0"
            try:
                country = user[-1]["country"]
                country = country["title"]
            except:
                country = "0"
            try:
                education = user[-1]["education"]
                education = education["university_name"]
            except:
                education = "0"
            try:
                occupation = user[-1]["occupation"]
                occupation = occupation["name"]
            except:
                occupation = "0"
            try:
                familyInt = user[-1]['relation']
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
                print(family)
            except:
                family = "0"
            try:
                birthday = user[-1]['bdate']
            except:
                birthday = '0'
            try:
                AlcoholInt = user[-1]['personal']['alcohol']
                if AlcoholInt == 1:
                    Alcohol = "резко негативное"
                elif AlcoholInt == 2:
                    Alcohol = "негативное"
                elif AlcoholInt == 3:
                    Alcohol = "компромиссное"
                elif AlcoholInt == 4:
                    Alcohol = "нейтральное"
                elif AlcoholInt == 5:
                    Alcohol = "положительное."
            except:
                Alcohol = "0"
            try:
                SmokeInt = user[-1]['personal']['smoking']
                if SmokeInt == 1:
                    Smoke = "резко негативное"
                elif SmokeInt == 2:
                    Smoke = "негативное"
                elif SmokeInt == 3:
                    Smoke = "компромиссное"
                elif SmokeInt == 4:
                    Smoke = "нейтральное"
                elif SmokeInt == 5:
                    Smoke = "положительное."
            except:
                Smoke = "0"
            try:
                politicalInt = user[-1]['personal']['political']
                if politicalInt == 1:
                    political = "коммунистические"
                elif politicalInt == 2:
                    political = "социалистические"
                elif politicalInt == 3:
                    political = "умеренные"
                elif politicalInt == 4:
                    political = "либеральные"
                elif politicalInt == 5:
                    political = "консервативные."
                elif politicalInt == 6:
                    political = "монархические"
                elif politicalInt == 7:
                    political = "ультраконсервативные"
                elif politicalInt == 8:
                    political = "индифферентные"
                elif politicalInt == 9:
                    political = "либертарианские."
            except:
                political = "0"
            try:
                interests = user[-1]['interests']
            except:
                interests = '0'
            #Добавляем в бд информацию по человеку
            #Затем добавляем комментарий в бд
            #меняем флаг переподсчета токсичности
        except:
            print('чет не получилось')



if __name__== '__main__':

    token = os.getenv("TOKEN")
    session = vk_api.VkApi(token=token)
    vk = session.get_api()

    print(f'Start {datetime.now()}\n')
    orm.create_tables()
    get_posts()
    
    print(f"\nStopped {datetime.now()}")

