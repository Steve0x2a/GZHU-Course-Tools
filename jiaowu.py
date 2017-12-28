import requests
from bs4 import BeautifulSoup
import getpass

class login_gzdx(object):
    def __init__(self):
        self.session = requests.session()
        self.baseUrl = 'http://202.192.18.184'
        self.url = 'https://cas.gzhu.edu.cn/cas_server/login?service=http%3a%2f%2f202.192.18.184%2fLogin_gzdx.aspx'
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    
    def login(self, account, passwd):
        self.username = account
        self.password = passwd
        lt, execution = self.get_webflow()
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
            print('成功')
            infourl = self.baseUrl+"/xsgrxx.aspx?xh="+account+"&"
            info = self.session.get(infourl)
            self.get_stuinfo(info)
            #text = self.session.get('http://my.gzhu.edu.cn/jw',headers = headers)
            '''text = self.session.get(jwurl,headers = headers)
            print(text.text)
        else:
            print(response.text)'''
    def get_webflow(self):
        response = self.session.get(url = self.url)
        soup = BeautifulSoup(response.text,'html.parser')
        lt = soup.find('input',{'name' : 'lt'})['value']
        execution = soup.find('input',{'name' : 'execution'})['value']
        soup.clear()
        return(lt,execution)

    def get_stuinfo(self,response):
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        d = {}
        d["studentnumber"] = soup.find(id="xh").string
        d["idCardNumber"] = soup.find(id="lbl_sfzh").string
        d["name"] = soup.find(id="xm").string
        d["sex"] = soup.find(id="lbl_xb").string
        d["enterSchoolTime"] = soup.find(id="lbl_rxrq").string
        d["birthsday"] = soup.find(id="lbl_csrq").string
        d["highschool"] = soup.find(id="lbl_byzx").string
        d["nationality"] = soup.find(id="lbl_mz").string
        d["hometown"] = soup.find(id="lbl_jg").string
        d["politicsStatus"] = soup.find(id="lbl_zzmm").string
        d["college"] = soup.find(id="lbl_xy").string
        d["major"] = soup.find(id="lbl_zymc").string
        d["classname"] = soup.find(id="lbl_xzb").string
        d["gradeClass"] = soup.find(id="lbl_dqszj").string
        for i in d:
            print('{}:{}'.format(i,d[i]))
        


if __name__ == '__main__':

    login = login_gzdx()
    account = input('输出学号')
    password = getpass.getpass("请输入您的密码:")
    login.login(account = account,passwd =password)

        

