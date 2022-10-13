from flask import Flask, render_template
import psycopg2
from flask_paginate import Pagination, get_page_args

con = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="123",
    host="127.0.0.1",
    port="5433"
)

cur = con.cursor()
app = Flask(__name__)


def get_Themes(offset=0, per_page=10, Themes = []):
    return Themes[offset: offset + per_page]

@app.route('/')
def home():
    return('hello world')

@app.route('/home')
def index():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    cur.execute("SELECT POSTTEXT,ROUND_TOXIC,COMMENTS_ID,POSTID,SIMMILAR from FILTRED")
    AllComments = cur.fetchall()
    total=len(AllComments)
    pagination_Themes = get_Themes(offset=offset, per_page=per_page, Themes=AllComments)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
    return render_template('base.html', comments=pagination_Themes, pagination=pagination, page=page, per_page=per_page)

if __name__ == '__main__':
    app.run(host='195.209.112.51', port=3000)
