from bs4 import BeautifulSoup
import re,json,requests,pickle,math
from sample.parse import get_stuinfo,get__VIEWSTATE2
from sample.account import jwlogin
from collections import OrderedDict


class course(jwlogin):


    def save_courses(self):
        '''
        用作储存选课表为data/course_list.json
        以及储存每个选课页面的viewstate用作选课
        '''
        self.login()
        course_url = self.baseUrl + "/xf_xsqxxxk.aspx?xh=" + self.username
        view = {}
        response = self.session.get(course_url)
        #用get__VIEWSTATE2函数获得首次访问选课页面viewstate以及viewgenerator参数
        state ,generator = get__VIEWSTATE2(response)
        #用get_total函数获得总课程数 再用math.ceil函数获得向右取整的选课页数
        total_page = math.ceil(float(self.get_total(response)/100))
        #为获得良好排序的课程表 故用OrderedDict
        courses_list = OrderedDict()
        courses_view ={}
        #获得每一页课程以及view参数
        for num in range(1,total_page+1) :
            got_course = self.get_courses_post(state,generator,num)
            now_course = self.get_coures_list(got_course,num)
            courses_list['第'+str(num)+'页'] = now_course
            now_view = self.get_courses_view(got_course,num)
            courses_view = dict(courses_view,**now_view)
        #保存gbk格式的名字以备后面使用
        courses_view['urlname'] = self.stuinfo['urlName'] 
        #将课程以及view参数保存下来以备使用
        with open('data/courses_list.json', 'w') as f:
            json.dump(courses_list, f,ensure_ascii=False,indent = 4, )
        with open('data/values/'+self.username+'view.txt', 'wb') as f:
            pickle.dump(courses_view,f)
        
    def get_coures_list(self,response,total_page):
        '''
        用正则表达式以及BS4获得课程表(待优化)
        '''
        soup = BeautifulSoup(response.text,'lxml')
        pattern =  re.compile('\d+')
        pattern2 = re.compile('kcmcGrid:_ctl\d+:jc')
        coursename = soup.find_all('input',type = 'checkbox' , attrs={'name' : re.compile(pattern2)} )
        course = OrderedDict()
        for i in coursename :
            classes = OrderedDict()
            course_id = str(total_page)+re.findall(pattern,i['id'])[0]
            name = i.find_parent('td').find_next('td').string
            code = name.next_element.string
            teacher_name = code.next_element.string
            course_time = teacher_name.next_element.string
            course_location = course_time.next_element.string
            course_code = course_location.next_element.string 
            total = course_code.next_element.string.next_element.string.next_element.string
            can_choose = total.next_element.string
            classes['课程名称'] = name
            classes['课程代码'] = code
            classes['教师'] = teacher_name
            classes['上课时间'] = course_time
            classes['上课地点'] = course_location
            classes['容量'] = total
            classes['剩余'] = can_choose
            course[course_id] = classes
        return course
            

    def get_courses_view(self,response,total_page):
        '''返回当前页的view参数'''
        __VIEWSTATE, __VIEWSTATEGENERATOR = get__VIEWSTATE2(response)
        view = {}
        view['state'+str(total_page)] = __VIEWSTATE
        view['generator'+str(total_page)] = __VIEWSTATEGENERATOR
        return view

    def get_total(self,response):
        '''获得可选课程总数'''
        soup = BeautifulSoup(response.text,'lxml')
        total_course = int(soup.find('span',id="dpkcmcGrid_lblTotalRecords").string)
        return total_course



    def get_courses_post(self,state,generator,index1):
        '''发出获取某页课程表请求'''
        data = {    
            '__EVENTTARGET': 'dpkcmcGrid:txtPageSize',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE':state,
            "__VIEWSTATEGENERATOR" : generator,
            'ddl_kcxz': '',
            'ddl_ywyl': '%D3%D0',
            'ddl_kcgs': '',
            'ddl_xqbs': '1',
            'ddl_sksj': '',
            'TextBox1': '',
            'dpkcmcGrid:txtChoosePage': index1,
            'dpkcmcGrid:txtPageSize': '100',
            'dpDataGrid2:txtChoosePage':'1',  
            'dpDataGrid2:txtPageSize':'100'
        }
        url = self.baseUrl + "/xf_xsqxxxk.aspx?xh=" + self.username
        response = self.session.post(url,data=data)
        return response

    def wx_save_courses(self,password):
        self.login()
        #构造选课链接url 其中urlName为gbk格式的姓名
        course_url = self.baseUrl + "/xf_xsqxxxk.aspx?xh=" + self.username
        view = {}
        response = self.session.get(course_url)
        #用get__VIEWSTATE2函数获得首次访问选课页面viewstate以及viewgenerator参数
        state ,generator = get__VIEWSTATE2(response)
        #用get_total函数获得总课程数 再用math.ceil函数获得向右取整的选课页数
        total_page = math.ceil(float(self.get_total(response)/100))
        courses_view ={}
        #获得每一页课程以及view参数
        for num in range(1,total_page+1) :
            got_course = self.get_courses_post(state,generator,num)
            now_view = self.get_courses_view(got_course,num)
            courses_view = dict(courses_view,**now_view)
        courses_view['password'] = password 
        #将课程以及view参数保存下来以备使用
        with open('data/values/'+self.username+'view.txt', 'wb') as f:
            pickle.dump(courses_view,f)
