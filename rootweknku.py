import json
from pip import main
from pymysql.cursors import DictCursor
import requests
from requests.cookies import RequestsCookieJar
import requests.utils
from bs4 import BeautifulSoup
import os
import sys
import re
import pymysql
import logging
LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s  %(message)s "#配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S' #配置输出时间的格式，注意月份和天数不要搞乱了



class wenku():
    def __init__(self,filename=None) -> None:
        self.cookies = RequestsCookieJar()
        self.headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        # self.uid = uid
        # self.pwd = pwd
        # proxy='127.0.0.1:1091' 
        # self.proxies={
        #     'http':'http://'+proxy,
        #     'https':'https://'+proxy
        # }
        self.filename = './static/img/'
        if filename:
            self.filename = filename
        if not os.path.exists(self.filename):
            os.mkdir(self.filename)
        host, user, passwd, database = '81.68.92.89', 'pipi', 'pipiAiqiq1_', 'db'
        self.conn = pymysql.connect(host=host,user=user,password=passwd,database=database,autocommit=False,cursorclass=DictCursor)
        self.cur = self.conn.cursor()
        pass

    def response_text(self,url):
        """请求函数"""
        response = requests.get(url,headers=self.headers,cookies=self.cookies) # 发送请求带入cookies
        if response.status_code==200:
            response.encoding="gbk"
        result = response.text
        self.cookies.update(response.cookies) #更新cookies
        return result
    
    def getnovel(self,bookid):
        booknovel = 'https://www.wenku8.net/book/{}.htm'.format(bookid)
        response = requests.get(booknovel,headers=self.headers)
        response.encoding = 'gbk'
        soup = BeautifulSoup(response.text,'html.parser')
        main_txt = soup.find('div',id='content')#这个里面有两个div 我们要第一个
        # print(main_txt)
        if not main_txt:
            return False
        # return False
        lp = main_txt.find('div')
        lp2 = lp.find_all('table',recursive=False)#有两个table 小说标题和作者在第一个里面 图片 tag 小说简介在第二个
        lp3 = lp2[0].find_all('tr',recursive=False)
        # print(lp3)
        novel_title = lp3[0].td.table.tr.td.span.b.string
        # print(novel_title)
        novel_auther = lp3[1].find_all('td')[1].string.split('：')[1].strip()
        # print(novel_auther)
        lp4 = lp2[1].tr.find_all('td',recursive=False)#这里面有是图片 tag 小说简介以及本书公告
        img_url = lp4[0].img['src']
        lp5 = lp4[1].find_all('span')#这里面是 tag 小说简介和公告
        if len(lp5) == 4:
            return False
        tag = lp5[0].b.string.split('：')[1].strip()#tag一定是第一个所以没问题 tag是根据；划分成两个区域 取第二个 去前后空格 所以tag是String对象
        jianjie = lp5[-1].get_text()#这里简介要注意 能爬的 是6个span 不能动是4个span
        # print(img_url,tag,jianjie)
        # novel = {'title': novel_title, 'cover': img_url, 'author': novel_auther, 'tag': tag, 'preivew': jianjie, 'hot': '0'}
        img_url = self.saveimage(img_url)
        novel = (novel_title,img_url,novel_auther,tag,jianjie,'0')
        # if not os.path.exists(self.filename+novel[0]):
        #     os.mkdir(self.filename+novel[0])
        return self.saveNovel(novel)

    def saveNovel(self, novel):
        q = 'insert into novel (title,cover,author,tag,preview,hot) values (%s,%s,%s,%s,%s,%s)'
        self.cur.execute(q, novel)
        id = self.conn.insert_id()
        self.conn.commit()
        return id

    def saveScroll(self, novel_id, name):
        q = 'insert into scroll (novel_id, scroll_name) values (%s,%s)'
        self.cur.execute(q, (novel_id, name))
        novel_id = self.conn.insert_id()
        self.conn.commit()
        return novel_id
    
    def saveTxt(self,novel_id, title, txt, chatu):
        q = 'insert into chapter (scroll_id, chapter_name, txt, chatu) values (%s, %s, %s, %s)'
        self.cur.execute(q, (novel_id, title, txt, chatu))
        self.conn.commit()

    def getbook(self,bookid):
        a = int(bookid // 1000)
        pbookid = self.getnovel(bookid=bookid)#这里可能两个结果 int id或者Flase
        if not pbookid:
            print(bookid,'完全不行')
            logging.info(str(bookid)+'完全不行')
            return 
        rbookid = str(pbookid)
        booknovel = "https://www.wenku8.net/novel/{}/{}/index.htm".format(a,bookid)
        print(booknovel+"这次要看的书")
        bookrespronse = requests.get(booknovel,headers=self.headers,cookies=self.cookies)
        bookrespronse.encoding = "gbk"
        soup = BeautifulSoup(bookrespronse.text,'html.parser')
        bookname = soup.find('div',id="title").string#获取标题
        print(bookname)
        # if not os.path.exists(self.filename+rbookid):
        #     os.mkdir(self.filename+rbookid)
        #获取章节
        all_chapter = soup.find('table')
        # print('all_chapter',all_chapter)
        self.getchapter(all_chapter,rbookid,bookid)

    def getchapter(self,all_chapter,bookname,bookid):#这里bookname 由数据库唯一指定id 也就是rbookid巨顶
        a = int(bookid // 1000)
        filename = self.filename + str(bookname) + '/'
        filename1, novel_id = '', 0
        tr_list = all_chapter.find_all('tr')
        for i in tr_list:
            td_list = i.find_all('td')
            print('td_list',td_list)
            for j in td_list:
                # print(j['class'])
                if j['class'][0] == 'vcss':
                    novel_id = self.saveScroll(str(bookname), j.string.strip())
                    # filename1 = filename+j.string.strip() #filename = /book/rbooid/
                    # if not os.path.exists(filename1):
                    #     os.mkdir(filename1)
                    continue
                else:
                    if j.a != None:
                        s = j.a['href'][:-4]
                        self.gettxt('https://www.wenku8.net/novel/{}/{}/{}.htm'.format(a,bookid,s),filename1,j.a.string,novel_id)
        return

    def gettxt(self,url,filename,chapter_name,novel_id):#获取章节内容并写入 
        a = self.response_text(url)
        soup = BeautifulSoup(a,'html.parser')
        # chapter_title = soup.find('div',id='title').string#获取了章节标题 一般为 卷名+标题的形式
        soup1 = soup.find("div",id='content')
        chatu = []
        for biv in soup1.find_all('div'):
            # print(str(biv))
            b = self.getimage(str(biv),filename)
            if b:
                chatu.append(b)
            biv.decompose()
        for ul in soup1.find_all('ul'):
            ul.decompose()
        # filename = filename + '/{}'.format(n + ' '+ chapter_title)+'.txt'
        a = soup1.get_text()
        self.saveTxt(str(novel_id), chapter_name, a, json.dumps(chatu))
        return chapter_name+'ok'

    def getimage(self,p_img,filename):
        pattern = r'href="(.*?)"'
        img_href = re.findall(pattern,p_img)
        if img_href:
            return self.saveimage(img_href[0])
        else:
            return None
        # print(img_href)
        # print(img_href)x
        # print(i.a.img['src'])
        # return self.saveimage(img_href,filename)


    def saveimage(self,url):
        # os.chdir(filename)
        try:
            r = requests.get(url,headers=self.headers,cookies=self.cookies,timeout=100)
            p = re.split('\W+',url)
            file_path = self.filename  + p[-2] + '.' + p[-1]
            with open(file_path,"wb") as f:
                f.write(r.content)
            return file_path[1:]
        except Exception as e:
            print("图片不行")
            return ''
        
if __name__=='__main__':
    args = sys.argv
    if len(args) == 3:
        W = wenku(args[1])
    else:
        W = wenku()
    ids = args[-1].split(',')
    logging.basicConfig(level=logging.INFO,
                    format=LOG_FORMAT,
                    datefmt = DATE_FORMAT ,
                    filename="./logs/rootwenkun_{}_{}.log".format(ids[0],ids[1]) #有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    )
    for i in range(int(ids[0]),int(ids[1])+1):
        try:
            W.getbook(int(i))
            logging.info('第{}bookid抓取完毕'.format(i))
        except Exception as e:
            logging.error(e)
    # for id in ids:
    #     W.getbook(int(id))