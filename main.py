import requests
from parse import get_webflow,get_stuinfo
import getpass

class login_gzdx(object):
    def __init__(self):
        self.session = requests.session()
        self.baseUrl = 'http://202.192.18.184'
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
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
        get_lt = self.session.get(url = self.url)
        lt, execution = get_webflow(get_lt)
        postdata = {
            'username' : account,
            'password' : passwd,
            'lt' : lt,
            'execution' : execution,
            '_eventId' : 'submit',
            'submit' : '登录'
        }

        response = self.session.post(url = self.url, data = postdata)
        if response.status_code == requests.codes.ok:
            infourl = self.baseUrl+"/xsgrxx.aspx?xh="+account+"&"
            info = self.session.get(infourl)
            try:
            self.stuinfo = get_stuinfo(info)
            print("欢迎你, {}, 您的学号为:{}".format(self.stuinfo["name"],self.stuinfo["studentnumber"]))
            except AttributeError:
                print("密码错误")
                login(account = account,passwd =password)

if __name__ == '__main__':
    login = login_gzdx()
    account = input('输出学号')
    password = getpass.getpass("请输入您的密码:")
    login.login(account = account,passwd =password)




