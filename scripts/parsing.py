import vk_api
from time import sleep
import psycopg2

con = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="123",
    host="127.0.0.1",
    port="5433"
)

cur = con.cursor()
con.autocommit = True

try:
    print("Database opened successfully")
    cur.execute('''CREATE TABLE COMMENTS  
         (
         FIRSTNAME TEXT ,
         SEKONDNAME TEXT ,
         COMMENT TEXT,
         CITY TEXT,
         COUNTRY TEXT,
         EDUCATION TEXT,
         OCCUPATION TEXT,
         ID TEXT,
         POSTID INT,
         FAMILY TEXT,
         BIRTHDATE TEXT,
         POSTTEXT TEXT,
         ALCOHOL TEXT,
         SMOKE TEXT,
         POLITICAL TEXT,
         INTERESTS TEXT,
         GROUPID TEXT,
         POSTDATE TEXT
         )
         ''')
except:
    print("Не создана таблица")


session = vk_api.VkApi(token='698e97510f36f88ced18449a9aa25c9663b8e2eeb1f42a857c3c5c2a65be69d5d90b645e12313d090aad7')
vk = session.get_api()

LastAttemp = 0

text=""
name=''
lastname=''
def get_comments (group_id):
    try:
        cur.execute("SELECT POSTID,ID  from COMMENTS")
        AllComments = cur.fetchall()
    except:
        AllComments=0
    print(len(AllComments))
    global LastAttemp
    Wall= session.method('wall.get', {"owner_id": group_id})
    count= Wall["count"]
    print(count)
    j=0
    i=0
    k=100
    while j <count :
        ExitFlag = False
        for post in Wall['items']:
            j=j+1
           # if post['date'] <= 1633392055 :     ограничение по дате, мол, получить все посты до этого момента. Время в формате SuperTIme вроде так называется. Если не нужно, комменть эти две строки
          #      j=count+1
           #     break
            if i > k:
                ExitFlag = True
                print("Закончено по причине превышения комментов за раз")
                break
            post_text=post['text']
            print("Пост номер ", post['id']) #Выписывать номер текущего поста, чтобы понимать, на каком сейчас месте программа
            comments = session.method('wall.getComments', {"owner_id": group_id, "post_id": post['id'], "extended":1 })
            post_id=post['id']
            ident= str('group_id') + '_' + str('j')
            posts = session.method('wall.getById', {"posts": ident })
            for comment in (comments["items"]):
                try:
                    i += 1
                    ExitFlag = False
                    from_id = comment["from_id"]
                    if from_id <= 0:
                        continue
                    print(comment["text"])
                    user = session.method("users.get", {"user_ids": from_id,"fields": "city,country,education,occupation,bdate,personal,relation,interests"})
                    name = user[-1]['first_name']
                    lastname = user[-1]['last_name']
                    CommentId=str(group_id)+"_"+str(comment['id'])
                    for b in range (len(AllComments)-1):
                        if AllComments[len(AllComments)-(b+1)][1]==CommentId:
                            ExitFlag = True
                            print("Совпадающий коммент")
                        if b >k+300:
                            break
                    if ExitFlag == True:
                        continue
                    try:
                        city = user[-1]["city"]
                        city=city["title"]
                    except:
                        city="0"
                    try:
                        country = user[-1]["country"]
                        country=country["title"]
                    except:
                        country="0"
                    try:
                        education = user[-1]["education"]
                        education=education["university_name"]
                    except:
                        education="0"
                    try:
                        occupation = user[-1]["occupation"]
                        occupation=occupation["name"]
                    except:
                        occupation="0"
                    try:
                        familyInt=user[-1]['relation']
                        if familyInt==1:
                            family="не женат/не замужем"
                        elif familyInt==2:
                            family="есть друг/есть подруга"
                        elif familyInt==3:
                            family="помолвлен/помолвлена"
                        elif familyInt==4:
                            family="женат/замужем"
                        elif familyInt==5:
                            family="всё сложно"
                        elif familyInt==6:
                            family="в активном поиске"
                        elif familyInt==7:
                            family="влюблён/влюблена"
                        elif familyInt==8:
                            family="в гражданском браке"
                        print(family)
                    except:
                        family="0"
                    try:
                        birthday=user[-1]['bdate']
                    except:
                        birthday='0'
                    
                    try:
                        AlcoholInt=user[-1]['personal']['alcohol']
                        if AlcoholInt==1:
                            Alcohol="резко негативное"
                        elif AlcoholInt==2:
                            Alcohol="негативное"
                        elif AlcoholInt==3:
                            Alcohol="компромиссное"
                        elif AlcoholInt==4:
                            Alcohol="нейтральное"
                        elif AlcoholInt==5:
                            Alcohol="положительное."
                    except:
                        Alcohol="0"
                    try:
                        SmokeInt=user[-1]['personal']['smoking']
                        if SmokeInt==1:
                            Smoke="резко негативное"
                        elif SmokeInt==2:
                            Smoke="негативное"
                        elif SmokeInt==3:
                            Smoke="компромиссное"
                        elif SmokeInt==4:
                            Smoke="нейтральное"
                        elif SmokeInt==5:
                            Smoke="положительное."
                    except:
                        Smoke="0"
                    try:
                        politicalInt=user[-1]['personal']['political']
                        if politicalInt==1:
                            political="коммунистические"
                        elif politicalInt==2:
                            political="социалистические"
                        elif politicalInt==3:
                            political="умеренные"
                        elif politicalInt==4:
                            political="либеральные"
                        elif politicalInt==5:
                            political="консервативные."
                        elif politicalInt==6:
                            political="монархические"
                        elif politicalInt==7:
                            political="ультраконсервативные"
                        elif politicalInt==8:
                            political="индифферентные"
                        elif politicalInt==9:
                            political="либертарианские."
                    except:
                        political="0"
                    try:
                        interests=user[-1]['interests']
                    except:
                        interests='0'
                    try:
                        postdate=str(post['date'])
                    except:
                        postdate='0'
                    myData = ({"first_name":name, "second_name":lastname,"comment":comment["text"],"city":city,"country":country,"education":education,"occupation":occupation,"comment_id":CommentId,"post_number":post_id, "family":family,"birthday":birthday,"post_text":post_text, "alcohol":Alcohol, "smoke":Smoke,"political":political,"interests":interests, "group_id":group_id, "postdate": postdate })
                    cur.execute ('INSERT INTO COMMENTS (FIRSTNAME,SEKONDNAME,COMMENT,CITY,COUNTRY,EDUCATION,OCCUPATION,ID,POSTID,FAMILY,BIRTHDATE,POSTTEXT,ALCOHOL, SMOKE, POLITICAL,INTERESTS,GROUPID,POSTDATE) VALUES (%(first_name)s,%(second_name)s,%(comment)s,%(city)s,%(country)s,%(education)s,%(occupation)s,%(comment_id)s,%(post_number)s,%(family)s,%(birthday)s,%(post_text)s,%(alcohol)s,%(smoke)s,%(political)s,%(interests)s,%(group_id)s,%(postdate)s)', myData)
                    if i > k:
                        ExitFlag = True
                        print("Закончено по причине превышения комментов за раз")
                        break
                except:
                    continue
            if ExitFlag == True:
                continue
            if i > k:
                ExitFlag = True
                print("Закончено по причине превышения комментов за раз")
                break
        break



groups=["-15755094","-26284064", "-51966513"]
while True:
    for group_id in groups:
        myData=get_comments(group_id)
    print ('Цикл завершен')
    sleep(60)
