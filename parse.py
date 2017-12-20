from bs4 import BeautifulSoup

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
    return d

