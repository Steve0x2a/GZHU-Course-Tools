from bs4 import BeautifulSoup
import urllib.parse

def get_webflow(response):
    soup = BeautifulSoup(response.text,'html.parser')
    lt = soup.find('input',{'name' : 'lt'})['value']
    execution = soup.find('input',{'name' : 'execution'})['value']
    soup.clear()
    return(lt,execution)

def get_stuinfo(response):
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
    d["urlName"] = urllib.parse.quote_plus(d["name"].encode('gb2312'))
    return d

def get__VIEWSTATE(response):
    html = response.content.decode("gb2312")
    soup = BeautifulSoup(html, "html.parser")
    __VIEWSTATE = soup.findAll(name="input")[0]["value"]
    __VIEWSTATEGENERATOR  = soup.findAll(name="input")[1]["value"]
    return __VIEWSTATE, __VIEWSTATEGENERATOR


def getGrade(response):
    html = response.content.decode("gb2312")
    soup = BeautifulSoup(html, "html5lib")
    trs = soup.find(id="Datagrid1").findAll("tr")[1:]
    Grades = []
    for tr in trs:
        tds = tr.findAll("td")
        tds = tds[:2] + tds[3:5] + tds[6:9]
        oneGradeKeys = ["year", "term", "name", "type", "credit","gradePonit","grade"]
        oneGradeValues = []
        for td in tds:
            oneGradeValues.append(td.string)
        oneGrade = dict((key, value) for key, value in zip(oneGradeKeys, oneGradeValues))
        Grades.append(oneGrade)
    return Grades

def get__VIEWSTATE2(response):
    html = response.content.decode("gbk")
    soup = BeautifulSoup(html, "html.parser")
    __VIEWSTATE = soup.findAll(name="input")[2]["value"]
    __VIEWSTATEGENERATOR  = soup.findAll(name="input")[3]["value"]
    return __VIEWSTATE, __VIEWSTATEGENERATOR
