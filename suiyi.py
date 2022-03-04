import pymysql
from pymysql.cursors import DictCursor


host, user, passwd, database = '81.68.92.89', 'pipi', 'pipiAiqiq1_', 'db'
db  = pymysql.connect(host=host,user=user,password=passwd,database=database,autocommit=True,cursorclass=DictCursor)
curs = db.cursor()

def qiantao(arr):
    rt = {}
    # print(arr)
    # for obj in arr:
    #     if obj[k] not in rt:
    #         rt[obj[k]] = []
    #         for j in range(len(outer)):
    #             outk = outer[j]
    #             rt[outk] = obj[outk]
    #     inn = rt[obj[k]]
    #     iobj = {}
    #     for j in range(len(inner)):
    #         innk = inner[j]
    #         iobj[innk] = obj[innk]
    #     inn.append(iobj)
    # print(rt)
    for a in arr:
        if a['scroll_name'] not in rt:
            rt[a['scroll_name']] = []#这里面装该卷下面的所有chapterid 以及chapter_name
        b = {'chapterid':a['chapterid'],'chapter_name':a['chapter_name']}
        rt[a['scroll_name']].append(b)
    # print(rt)
    return rt

def novelfind(id):
    a = "select * from novel where id = %s"
    curs.execute(a,id)
    return curs.fetchone()

def scrollfind(id):
    a = """select scroll.scroll_name as scroll_name, chapter.id as chapterid, chapter.chapter_name as chapter_name from scroll left join chapter 
    on scroll.id = chapter.scroll_id where novel_id = %s order by chapterid"""
    curs.execute(a,id)
    return qiantao(curs.fetchall())

def chapterfind(id):
    #chapterid ,scroll.novel_id ,scroll.scroll_name
    a = "select chapter.*, scroll.scroll_name,scroll.novel_id as nid from chapter left join scroll on chapter.scroll_id = scroll.id where chapter.id = %s"
    curs.execute(a,id)
    return curs.fetchone()

def getrank10():
    #随机10本
    a = "select id,cover,title from novel order by rand() LIMIT 10"
    curs.execute(a)
    return curs.fetchall()

def next_chapter(novel_id,chapter_id,fangxiang):#这里三个参数 方向为string 字符
    a = "select chapter.id from novel,scroll,chapter where %s = novel.id and chapter.scroll_id = scroll.id and scroll.novel_id = novel.id and chapter.id {} %s order by chapter.id {} limit 1"
    flag = 'asc'
    if fangxiang == '<':
        flag = 'desc'
    a = a.format(fangxiang,flag )
    # print(a)
    curs.execute(a,(novel_id,chapter_id))
    return curs.fetchone()

def search_book(keyword,cp,page:int):
    a = 'SELECT id,title,cover FROM novel WHERE {} LIKE %s limit %s,10'.format(cp)
    # print(a, keyword)
    curs.execute(a,('%'+keyword+'%',page*10))
    return curs.fetchall()

def search_book2(keyword,cp):#用来查最大页数
    a = 'select count(id) as cid from novel where {} like %s'.format(cp)
    curs.execute(a,('%'+keyword+'%'))
    return curs.fetchone()#返回cid 是查询出来的所有数目

def getnovelnames(ids):#参数是int 元组
    a = 'select id,title from novel where id in (%s)'%','.join(["%s"]*len(ids))
    curs.execute(a,ids)
    return curs.fetchall()

def getChaptername(ids):
    a = 'select id,chapter_name from chapter where id in (%s)'%','.join(["%s"]*len(ids))
    curs.execute(a,ids)
    return curs.fetchall()
    ###目前为止这两个方法很好用 受限表设计问题 好的

# print(next_chapter(1,15,'<'))
# print(getnovelnames((1,2,3,4,5)))
# print(['%s']*3)