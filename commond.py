# import math
# from aiohttp import request
from re import S
from flask import Flask,render_template,redirect,request
# from flask import render_template
# import pymysql
# from pymysql.cursors import DictCursor
# pymysql.install_as_MySQLdb()
# from flask_sqlalchemy import SQLAlchemy
from suiyi import *
import json


app = Flask(__name__,static_folder='static',static_url_path='/static')
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
    uls = getrank10()
    #主页 2022.12开工
    return render_template('/index.html',title="伪轻小说文库,抄袭第一名",uls=uls)

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

@app.route('/page/<int:nid>/<int:cid>/<fangxiang>')
def page(nid,cid,fangxiang):
    flag = '>'
    if fangxiang != 'next':
        flag = '<'
    a = next_chapter(nid,cid,flag)
    if not a:
        url = '/novel/{}/index'.format(nid)
    else:
        url = '/novel/{}/{}'.format(nid,a.get('id'))
    print(url)
    return redirect(url)

@app.route('/search',methods=['GET','POST'])
def search():
    #这刷搜索功能 表单两个参数
    # print(request.form)
    # print(request.method)
    page = 0
    if request.method == 'GET':
        keyword = request.args.get('keyword')
        cp = request.args.get('cp')#类别 0 1
        page = int(request.args.get('page'))
    else:
        keyword = request.form.get('keyword')
        cp = request.form.get('cp')#类别 0 1
    if not int(cp):
        s = 'title'
    else:
        s = 'author'
        # str.strip()
    if keyword:
        a = search_book(keyword=keyword.strip(),cp=s,page=page)
        # print(a)
        if len(a) == 1:
            return redirect('/jianjie/{}'.format(a[0].get('id')))#如何是单个查询结果则301到简介页面
        # b = (keyword,cp,page)
        b1 = 'keyword={}&cp={}&page={}'
        bb1 = b1.format(keyword,cp,page-1 if page-1 >= 0 else 0)
        c1 = int((search_book2(keyword=keyword.strip(),cp=s).get('cid'))+9.5)//10 - 1#这是最大页数
        bb2 = b1.format(keyword,cp,page+1 if page+1 <= c1 else c1)

        return render_template('/search.html',title=keyword+'搜索结果',uls=a,three=(bb1,bb2))
    else:
        return '我劝你善良'

    






if __name__ == '__main__':
    app.run(host='0,0,0,0',port = 5000,debug=True)