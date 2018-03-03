import requests
from threading import Thread
import sys
import queue
import urllib.parse
import pickle
from sample.parse import get_selected_course

class select_course(object):


    def __init__(self,index1='',index2='',username,MAX,TIMEOUT):
        '''
        初始化一些参数
        max为队列倍数
        index1 index2分别为选课页数和在课程在页数上的序号 用作发出选课请求
        view字典里储存着之前获取的每个页面的view参数 可快速进行抢课而不用等待解析
        urls是当前可用选课服务器
        data是发出选课post所需参数
        '''
        self.concurrent = 200
        self.q = queue.Queue(self.concurrent * 2)
        self.username = username
        self.timeout = TIMEOUT
        self.max = MAX
        self.index1, self.index2 = index1,index2
        self.response = ''
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
        'http://202.192.18.183',
        'http://202.192.18.184',
        'http://202.192.18.182'
        ]*self.max
        self.data = {
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE':view['state'+self.index1],
                "__VIEWSTATEGENERATOR" : view['generator'+self.index1],
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
                url = self.q.get()
                response = self.session.post(url,data = self.data,timeout = self.timeout)
                if response.status_code == 200:
                    self.response = response                            
                self.selected = self.get_selected_course(response)
                self.q.task_done()
            except:
                self.q.task_done()
                
    def run(self):
        for i in range(self.concurrent):
            t = Thread(target=self.post)
            t.daemon = True
            t.start()
        try:
            for host in self.urls:
                url = host+'/xf_xsqxxxk.aspx?xh='+self.username+'&xm='+self.view['urlname']+'&gnmkdm=N121203'
                self.q.put(url.strip())
            self.q.join()
        except KeyboardInterrupt:
            sys.exit(1)

    def show_selected(self):
        try:
            courses = get_selected_course(self.response)
            print('已选课程:{}'.format(courses))
        except :
            url="http://202.192.18.184/xf_xsqxxxk.aspx?xh='+self.username"
            response = self.session.get(url)
            courses = get_selected_course(response)
            print('选课出错,已选课程:{}'.format(courses))            
                
            
