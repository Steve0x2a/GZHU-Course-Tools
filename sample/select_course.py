import requests
from threading import Thread
import sys
import queue
import urllib.parse
import pickle

class select_course(object):


    def __init__(self,index1,index2,MAX):
        '''
        初始化一些参数
        max为队列倍数
        index1 index2分别为选课页数和在课程在页数上的序号 用作发出选课请求
        view字典里储存着之前获取的每个页面的view参数 可快速进行抢课而不用等待解析
        urls是当前可用选课服务器
        data是发出选课post所需参数
        '''
        self.max = MAX
        self.index1, self.index2 = index1,index2
        self.session = requests.session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) \
                                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        with open('data/cookies/'+ self.username +'.txt','rb') as f:
            cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
        self.session.cookies = cookies
        with open('data/values/'+self.username+'view.txt', 'rb') as f:
            view = pickle.load(f)
        self.view = view
        self.urls = [
        'http://202.192.18.189',
        'http://202.192.18.183',
        'http://202.192.18.184',
        'http://202.192.18.182'
        ]
        self.data = {
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE':view['state'+index1],
                "__VIEWSTATEGENERATOR" : view['generator'+index1],
                'ddl_kcxz': '',
                'ddl_ywyl': '',
                'ddl_kcgs': '',
                'ddl_xqbs': '1',
                'ddl_sksj': '',
                'TextBox1': '',
                'kcmcGrid:_ctl'+index2+':xk':'on',
                'Button1': urllib.parse.quote_plus('  提交  '.encode('gb2312')),
                'dpkcmcGrid:txtChoosePage': index1,
                'dpkcmcGrid:txtPageSize': '100',
                'dpDataGrid2:txtChoosePage':'1',  
                'dpDataGrid2:txtPageSize':'100'

            }
            
    def post(self):
        '''发出选课请求函数 用作被run函数调用'''
        while True:    
            try:
                url = q.get()
                self.session.post(url,data = self.data)
                q.task_done()
            except:
                q.task_done()
                
    def run(self):
        '''线程队列发出post 可异步请求 极高效率进行post选课请求'''
        concurrent = 200
        q = queue.Queue(concurrent * 2)
        urls = self.urls * self.max
        for i in range(concurrent):
            t = Thread(target=self.post)
            t.daemon = True
            t.start()
        try:
            for url in urls:
                q.put(url.strip())
            q.join()
        except KeyboardInterrupt:
            sys.exit(1)
        
