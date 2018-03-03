from sample import account,get_course,select_course
import fire,pickle

class Run(object):
    '''
    使用方法:
    refresh 学号 教务密码 刷新cookies以及课程表
    select index 线程数 开始抢课
    '''
    def __init__(self,MAX = 10,TIMEOUT = 7):
        self.TIMEOUT = TIMEOUT
        self.MAX = MAX
    def refresh(self,username,password):
        username = str(username)
        passwoed = str(password)
        get = get_course.course(username,password)
        get.save_courses()
    def select(self,username,index):
        username = str(username)
        index = str(index)
        index1 = index[0]
        index2 = index[1:]
        sc = select_course.select_course(index1,index2,username,self.MAX,self.TIMEOUT)
        flag = 1
        while flag==1:
            sc.run()
            sc.show_selected()
            flag = int(input('选课成功请输入0退出 输入1重复选课操作 '))
    def file(self,method):
        with open("info.json",'r') as f:
            info = json.load(f)
        method = str(method)
        if method == "refresh":
            jwlogin = jw.login(info["username"],info["password"])
            jwlogin.main()
            get = get_course.course(info["username"])
            get.save_courses()
        if method == "select":
            index1 = info["index"][0]
            index2 = info["index"][1:]
            sc = select_course.select_course(index1,index2,info["username"],self.MAX,self.TIMEOUT)
            flag = 1
            while flag==1:
                sc.run()
                sc.show_selected()
                flag = int(input('选课成功请输入0退出 输入1重复选课操作 '))     
            
class wxbot(Run):
    def wx_select(self,username,password,index):
        if self.ensure(username,password):
            index1 = index[0]
            index2 = index[1:]      
            sc = select_course.select_course(index1,index2,username,self.MAX,self.TIMEOUT)
            sc.run()
            return '已选课程'+sc.show_selected()
        else :
            return('密码错误')
    def wx_refresh(self,username,password):
        if self.ensure(username,password):
            jwlogin = account.login(username,password)
            res = jwlogin.account_login()
            return res
        else:
            return('密码错误')
    def wx_login(self,username,password):
        jwlogin = account.login(username,password)
        res = jwlogin.account_login()
        if res == 'Account login successfully':
            get = get_course.course(username)
            get.wx_save_courses(password)
        return res
    def wx_show(self,username,password):
        if self.ensure(username,password):
            sc = select_course.select_course(username = username,MAX = self.MAX,TIMEOUT = elf.TIMEOUT)
            sc.show_selected()
    def ensure(self,username,password):
        with open('data/values/'+username+'view.txt', 'rb') as f:
            view = pickle.load(f)
            if view['password'] == password:
                return True
            else:
                return False
               


if __name__ == '__main__':
  fire.Fire(Run)