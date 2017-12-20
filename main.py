import requests
from bs4 import BeautifulSoup
from parse import get_webflow

class login_gzdx(object):
    def __init__(self,headers):
        self.session = requests.session()
        self.headers = headers
        self.baseUrl = 'http://202.192.18.184'
        self.url = 'https://cas.gzhu.edu.cn/cas_server/login?service=http%3a%2f%2f202.192.18.184%2fLogin_gzdx.aspx'
    
    def login(self, account, passwd):
        self.username = account
        self.password = passwd
        get_lt = self.session.get(url = self.url,headers = self.headers)
        lt, execution = get_webflow(get_lt)
        postdata = {
            'username' : account,
            'password' : passwd,
            'lt' : lt,
            'execution' : execution,
            '_eventId' : 'submit',
            'submit' : '登录'
        }

        response = self.session.post(url = self.url, headers = self.headers, data = postdata)
        if response.status_code == requests.codes.ok:
            print('成功')
            infourl = self.baseUrl+"/xsgrxx.aspx?xh="+account+"&"
            info = self.session.get(infourl,headers = headers)
            self.get_stuinfo(info)
            #text = self.session.get('http://my.gzhu.edu.cn/jw',headers = headers)
            '''text = self.session.get(jwurl,headers = headers)
            print(text.text)
        else:
            print(response.text)'''
