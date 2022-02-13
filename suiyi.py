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
    a = "select id,cover,title from novel LIMIT 10"
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


# print(next_chapter(1,15,'<'))