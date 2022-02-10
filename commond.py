# import math
from flask import Flask,render_template,jsonify
# from flask import render_template
# import pymysql
# from pymysql.cursors import DictCursor
# pymysql.install_as_MySQLdb()
# from flask_sqlalchemy import SQLAlchemy
from suiyi import db,novelfind,scrollfind,chapterfind
import json


app = Flask(__name__,static_folder='static',static_url_path='')
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://pipi:pipiAiqiq1_@81.68.92.89:3306/db?charset=utf8"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# host, user, passwd, database = '81.68.92.89', 'pipi', 'pipiAiqiq1_', 'db'
# conn = pymysql.connect(host=host,user=user,password=passwd,database=database,autocommit=True,cursorclass=DictCursor)
# cur = conn.cursor()
# db = sqlalchemy(app)

# class Novel(db)
def pinjie(s:str):
    return s.endswith('\n')

@app.route('/chariter')
def hello_world():
    return render_template('/chariter.html')

@app.route('/') 
def index():
    title = 'hahaha'
    txt = ''
    with open('01.txt','r',encoding='utf-8') as f:
        c = f.readline()
        while c:
            txt += c
            if pinjie(c):
                txt += '<br>'
            c = f.readline()
    return render_template('/novel.html',title=title,txt=txt)

@app.route('/jianjie/<id>')
def jianjie(id):
    novel = novelfind(id)
    # print(novel)
    # cur.execute('select * from novel where id = %s', (id))
    # novel = cur.fetchone()
    # print(novel.preview)
    novel['preview']= novel['preview'].replace('\n', '</br>')
    # print(novel.preview, len(novel.preview))
    # for x in novel.preview:
    #     print(x + '|')
    return render_template('/jianjie.html',title=novel['title'],novel=novel)

@app.route('/novel/<id>/index')
def scroll(id):
    novel = novelfind(id)
    scrolls = scrollfind(id)
    # print(novel)
    # print(scrolls)
    return render_template('/scroll.html',title=novel['title'],scrolls=scrolls)

@app.route('/novel/<int:id>/<int:bid>')
def novel(id,bid):
    a = chapterfind(bid)
    print(id,a.get('nid'))
    if int(id) != a.get('nid'):
        return "404.html"
    a['txt'] = a['txt'].replace('\n', '<br/>')
    a['txt'] = a['txt'].replace('\xa0\xa0\xa0\xa0', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
    a['chatu'] = json.loads(a['chatu'])
    # novel = ChapterContent.query.get(bid)
    # novel.txt= novel.txt.replace('\n', '</br>')
    # novel.chatu = json.loads(novel.chatu)
    # print(novel.chatu)
    return render_template('/novel.html',title=a['scroll_name'],novel=a)





if __name__ == '__main__':
    app.run(host='0,0,0,0',port = 5000,debug=True)