import requests
from parse import get_webflow,get_stuinfo
import getpass

class login_gzdx(object):
    def __init__(self,headers):
        self.session = requests.session()
        self.headers = headers
        self.baseUrl = 'http://202.192.18.184'
        self.url = 'https://cas.gzhu.edu.cn/cas_server/login?service=http%3a%2f%2f202.192.18.184%2fLogin_gzdx.aspx'
        self.stuinfo = {}

    def login(self, account, passwd):
        '''

        :param account: 传入学号
        :param passwd:传入密码
        :模拟登陆主要部分
        '''
        self.username = account
        self.password = passwd
        get_lt = self.session.get(url = self.url, headers = self.headers)
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
            self.stuinfo = get_stuinfo(info)
            print("欢迎你, {}, 您的学号为:{}".format(self.stuinfo["name"],self.stuinfo["studentnumber"]))

if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
    }
    login = login_gzdx(headers = headers)
    account = input('输出学号')
    password = getpass.getpass("请输入您的密码:")
    login.login(account = account,passwd =password)




