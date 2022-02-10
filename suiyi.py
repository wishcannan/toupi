import pymysql
from pymysql.cursors import DictCursor


host, user, passwd, database = '255.255.255.255', 'user', 'passwd', 'db'
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
    #chapterid
    a = "select chapter.*, scroll.scroll_name,scroll.novel_id as nid from chapter left join scroll on chapter.scroll_id = scroll.id where chapter.id = %s"
    curs.execute(a,id)
    return curs.fetchone()

