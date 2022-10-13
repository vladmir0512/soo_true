import psycopg2
from array import *
from nltk.corpus import stopwords
from time import sleep

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
    cur.execute('''CREATE TABLE FILTRED
         (
         POSTTEXT TEXT ,
         ROUND_TOXIC TEXT,
         COMMENTS_ID TEXT,
         POSTID TEXT,
         SIMMILAR TEXT
         )
         ''')
except:
    print("Не создана таблица")

def get_corpus(data):
    corpus = []
    for word in data.split():
        corpus.append(word)
    return corpus

def str_corpus(corpus):
    str_corpus = ''
    for i in corpus:
        str_corpus += ' ' + i
    str_corpus = str_corpus.strip()
    return str_corpus

def Analizing(SortedList,y):
    SimmilarPosts=[]
    for z in range(y-100,y+100):
        print(z)
        print(y)
        if z==y:
            continue
        if y>=len(SortedList):
            break
        if z>=len(SortedList) or z<0:
            break
        text1=get_corpus(SortedList[y][0])
        text2=get_corpus(SortedList[z][0])
        print(text1)
        print(text2)
        text1 = list(map(lambda x: x.lower(), text1))
        text2 = list(map(lambda x: x.lower(), text2))
        a=len(text1)
        b=len(text2)
        num_words1 = len(set(text1))
        num_words2 = len(set(text2))
        num=num_words1+num_words2
        for i in range (a):
            for j in range(i+1,a):
                if text1[i]==text1[j] or text1[i]=="":
                    text1[j]=""
            if text1[i] in stopwords.words('russian'):
                text1[i]=""
            if text1[i]=="." or text1[i]=="-" or text1[i]=="?" or text1[i]=="!" or text1[i]=="...":
                    text1[i]=""
        i=0
        Z=0
        for i in range (b):
            for j in range(i+1,b):
                if text2[i]==text2[j]:
                    text2[j]=""
            if text2[i] in stopwords.words('russian'):
                text2[i]=""
            if text2[i]=="." or text2[i]=="-" or text2[i]=="?" or text2[i]=="!" or text2[i]=="...":
                text2[i]=""
        for i in range (a):
            for j in range(b):
                if text1[i]==text2[j] and text1[i]!="":
                    num=num-1
                    Z=Z+1
        try:
            perc=(Z/num)*100
        except:
            perc=0
        if perc>10:
            SimmilarPosts.append(SortedList[z][1])
        else:
            pos=0
    return(SimmilarPosts)

def get_Themes(offset=0, per_page=10, Themes = []):
    return Themes[offset: offset + per_page]


def index():
    cur.execute("DROP TABLE IF EXISTS FILTRED")
    try:
        print("Database opened successfully")
        cur.execute('''CREATE TABLE FILTRED
             (
             POSTTEXT TEXT ,
             ROUND_TOXIC TEXT,
             COMMENTS_ID TEXT,
             POSTID TEXT,
             SIMMILAR TEXT
             )
             ''')
    except:
        print("Не создана таблица")
    SortedList=[]
    Simmilar_post=[]
    cur.execute("SELECT POSTTEXt,ID,POSTID,POSTDATE  from COMMENTS ORDER BY POSTDATE")
    AllComments = cur.fetchall()
    for i in range(len(AllComments)):
        if i == 0:
            Simmilar_post.append(AllComments[i][0])
            groupid1=AllComments[i][1].split('_')[0]
            groupid=groupid1.split('-')[1]
            postlink=("https://vk.com/public"+str(groupid)+"?w=wall-"+str(groupid)+"_"+str(AllComments[i][2]))
            Simmilar_post.append(postlink)
        Simmilar_post.append(AllComments[i][1])   
        if i==(len(AllComments)-1):
            SortedList.append(Simmilar_post)
            break
        if AllComments[i][2]!=AllComments[i+1][2]:
            SortedList.append(Simmilar_post)
            Simmilar_post=[]
            Simmilar_post.append(AllComments[i+1][0])
            groupid1=AllComments[i+1][1].split('_')[0]
            groupid=groupid1.split('-')[1]
            postlink=("https://vk.com/public"+str(groupid)+"?w=wall-"+str(groupid)+"_"+str(AllComments[i+1][2]))
            Simmilar_post.append(postlink)
    cur.execute("SELECT ID,TOXIC  from TOXIC")
    toxicTable=cur.fetchall()
    count=0
    need=0
    Themes=[]
    #Themes=[["Post 1","0.5","10"],["Post 2","0.5","10"],["Post 3","0.5","10"],["Post 4","0.5","10"],["Post 5","0.5","10"],["Post 6","0.5","10"],["Post 7","0.5","10"],["Post 8","0.5","10"],["Post 9","0.5","10"],["Post 10","0.5","10"],["Post 11","0.5","10"],["Post 12","0.5","10"],["Post 13","0.5","10"],["Post 14","0.5","10"],["Post 15","0.5","10"]]
    for k in range(len(SortedList)):
        Theme=[]
        count=0
        need=0
        for i in range(len(SortedList[k])):
            if i==0 or i==1:
                continue
            for j in range(len(toxicTable)):
                if SortedList[k][i]==toxicTable[j][0]:
                    count+=1
                    need=need+float(toxicTable[j][1])
        if len(SortedList[k][0])>200:
            SortedList[k][0]=SortedList[k][0][:200]+"..."
        SimmilarPosts=Analizing(SortedList,k)
        Theme.append(SortedList[k][0])
        if count==0:
            Theme.append("Средняя токсичность - 0")
        else:
            Theme.append("Средняя токсичность - "+str(round(need/count,2)))
        Theme.append("Комментариев: "+str(count))
        Theme.append(SortedList[k][1])
        Theme.append(SimmilarPosts)
        Themes.append(Theme)
        myData = ({"post_text":Theme[0], "toxic":Theme[1],"comments":Theme[2],"post_id":Theme[3],"simmilar":Theme[4]})
        cur.execute ('INSERT INTO FILTRED (POSTTEXT,ROUND_TOXIC,COMMENTS_ID,POSTID,SIMMILAR) VALUES (%(post_text)s,%(toxic)s,%(comments)s,%(post_id)s,%(simmilar)s)', myData)

while True:
    index()
    print("цикл завершен")
    sleep(3600)
