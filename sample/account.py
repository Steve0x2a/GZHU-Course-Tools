import requests,pickle,urllib.parse
from sample.parse import get_webflow,get_stuinfo,get__VIEWSTATE,get__VIEWSTATE2

class jwlogin(object):


    def __init__(self,username,password,timeout = 7):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.baseUrl = 'http://202.192.18.183'
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        self.loginurl = 'https://cas.gzhu.edu.cn/cas_server/login?service=http%3a%2f%2f202.192.18.183%2fLogin_gzdx.aspx'
        self.timeout = timeout
        self.infourl = self.baseUrl+"/xsgrxx.aspx?xh="+self.username+"&"  

    def login(self):
        '''
        :先尝试使用cookie登录 失败则使用账号密码登录并且储存cookie
        '''
        try:
            res = self.cookie_login()
            return res
        except:
            res = self.account_login()  
            return res

    def cookie_login(self):
        '''
        :使用cookie登录
        '''
        with open('data/cookies/'+ self.username +'.txt','rb') as f:
            cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
        self.session.cookies = cookies
        response = self.session.post(url = self.loginurl, timeout = self.timeout)
        info = self.session.get(self.infourl, timeout = self.timeout)
        self.stuinfo = get_stuinfo(info)
        print("欢迎你, {}, Cookie登录成功。您的学号为:{}".format(self.stuinfo["name"],self.stuinfo["studentnumber"]))
        
    def account_login(self):
        '''
        :使用账号密码模拟登录 并且存储cookie
        '''
        #获得登录表格所需的值
        get_lt = self.session.get(url = self.loginurl)
        lt, execution = get_webflow(get_lt)
        #构建post表单
        postdata = {
            'username' : self.username,
            'password' : self.password,
            'lt' : lt,
            'execution' : execution,
            '_eventId' : 'submit',
            'submit' : '登录'
        }
        #用requests post模拟登陆
        try:
            response = self.session.post(url = self.loginurl, data = postdata, timeout = self.timeout)
        #若返回response中有xs_main.aspx项则证明登录成功
            if "xs_main.aspx" in response.text:
                #获得登陆者信息
                info = self.session.get(self.infourl)
                self.stuinfo = get_stuinfo(info)
                #将cookie转为文件储存
                with open('data/cookies/'+self.username+'.txt', 'wb+') as f:
                    pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)
                return 'Account login successfully'
            elif "密码错误" in response.text:
                return 'Got a wrong password'
            else:
                return 'Got a unknown error'
        except requests.exceptions.Timeout:
            return 'TimeOut!'