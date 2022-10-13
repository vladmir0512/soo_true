import psycopg2
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
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

print('connect!')
try:
    cur.execute('''CREATE TABLE TOXIC  
            (
                ID text,
                TOXIC text
            )
            ''')
    print('create table!')
except:
    print('table not created!')

# def text2toxicity(text):
#         model_checkpoint = 'cointegrated/rubert-tiny-toxicity'
#         tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
#         model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)
#         if torch.cuda.is_available():
#             model.cuda()
#         """ Calculate toxicity of a text (if aggregate=True) or a vector of toxicity aspects (if aggregate=False)"""
#         with torch.no_grad():
#             inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(model.device)
#             proba = torch.sigmoid(model(**inputs).logits).cpu().numpy()
#         if isinstance(text, str):
#             proba = proba[0]
#         if (1 - proba.T[0] * (1 - proba.T[-1])) > 0.5:
#             return '1'
#         else:
#             return '0'

def text2toxicity(text):
        model_checkpoint = 'cointegrated/rubert-tiny-toxicity'
        tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
        model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)
        if torch.cuda.is_available():
            model.cuda()
        """ Calculate toxicity of a text (if aggregate=True) or a vector of toxicity aspects (if aggregate=False)"""
        with torch.no_grad():
            inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(model.device)
            proba = torch.sigmoid(model(**inputs).logits).cpu().numpy()
        if isinstance(text, str):
            proba = proba[0]    
        return 1 - proba.T[0] * (1 - proba.T[-1])

while True:
    cur.execute("SELECT ID, COMMENT from COMMENTS")
    data = cur.fetchall()
    print('selecting done!')   

    cur.execute("SELECT ID, TOXIC  from TOXIC")
    dbdata = cur.fetchall()
    print(dbdata)

    DataList=[]
    ExitFlag=False

    for i in range(len(data)):
        ExitFlag=False
        for y in range(len(dbdata)):
            print("Проверяем "+data[i][0]+ "  "+ dbdata[y][0])
            if data[i][0]==dbdata[y][0]:
                ExitFlag=True
                break
        if not ExitFlag: 
            print("Не совпало, добавляем:  "+ data[i][0])
            DataList=list(data[i])
            print(DataList)
            #оценить токсичность
            print(DataList[1])
            DataList[1] = text2toxicity(DataList[1])
            DataList = tuple(DataList)
            myData = ({"ID":DataList[0], "TOXIC":DataList[1]})
            cur.execute ('INSERT INTO TOXIC (ID,TOXIC) VALUES (%(ID)s,%(TOXIC)s)', myData)
            continue
        if ExitFlag:
            print('Совпало, не добавляем')
            continue
    sleep(60)
