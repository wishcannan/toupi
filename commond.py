from flask import Flask,render_template,redirect,request,jsonify,flash
from suiyi import *
import json
from werkzeug.utils import secure_filename
from noise import lp2 #这个是我噪声处理图片功能模块 参数只接受一个file
from redissuiyi import getredis #这个实现一个简单的连接池
import time
# import redis


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
    r=getredis()
    IP_Add = request.headers.get('X-Real-IP')
    # print(request.remote_addr)#这个获取request 访问ip
    if not r.exists('hotip'):
        a = time.time()+86400
        tomorow = time.mktime(time.strptime(time.strftime("%a %b %d 0:0:0 %Y",time.localtime(a))))
        r.sadd('hotip',IP_Add)
        r.incr('hot',1)
        r.expireat('hotip',int(tomorow))
    else:
        if not r.sismember('hotip',IP_Add):
            r.sadd('hotip',IP_Add)
            r.incr('hot',1)
    hot = str(r.get('hot'),encoding='utf-8')
    #主页 2022.12开工
    return render_template('/index.html',title="伪轻小说文库,抄袭第一名",uls=uls,hot=hot)

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

@app.route('/getnovelchaptername')
def qishenmefangfaming():
    novel_data = json.loads(request.args.get('data'))#这里是list里面大概是 [novelid_chapterid,]
    alist,blist,cdict = [],[],{}
    res= []
    for i in novel_data:
        a,b = i.split('_')
        alist.append(a)
        blist.append(b)
        cdict[str(a)] = b
    
    d = getnovelnames(tuple(alist))
    e = getChaptername(tuple(blist))
    for i in d:
        nid = i.get('id')
        cid = cdict.get(str(nid))
        r = {'id':nid, 'cid':cid, 'name':i.get('title')}
        for j in range(len(e)):
            if int(cid) == e[j]['id']:
                r['cname'] = e[j]['chapter_name']
                e.pop(j)
                break
        res.append(r)
    # print(res,'woderenwuwanchengl')
    return jsonify(res)

ALLOWED_EXTENSIONS = {'png','jpg','jpeg','bmp'}
def allowed_file(filename):
    #这个方法检测文件名是否符合我们要求的后缀
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):#
            filename = secure_filename(file.filename)
            # print('图片准备进去了')
            lp2(file,filename)
            # print('出来了')
            return render_template('upload.html',title='记得接受结果',img_filename='/static/img2/'+filename)
    else:
        return render_template('upload.html',title='Upload new File')
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', name=filename))
        
    






if __name__ == '__main__':
    app.run(host='localhost',port = 5000,debug=False)