from sample import jw,get_course,select_course,test
import fire

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
        jwlogin = jw.login(username,password)
        jwlogin.main()
        get = get_course.course(username)
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


if __name__ == '__main__':
  fire.Fire(Run)