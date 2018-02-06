from sample import jw,get_course,select_course
import fire
'''
username = '1719500024'
password = 'zhanyi051414'
jwlogin = jw.login(username,password)
#jwlogin.main()
get = get_course.course(username)
get.save_courses()'''
class Run(object):
    '''
    使用方法:
    refresh 学号 教务密码 刷新cookies以及课程表
    select index 线程数 开始抢课
    '''
    def refresh(username,password):
        jwlogin = jw.login(username,password)
        jwlogin.main()
        get = get_course.course(username)
        get.save_courses()
    def select(index,MAX = 10):
        index1 = index[0]
        index2 = index[1:]
        sc = select_course(index1,index2,MAX)
        sc.run()

if __name__ == '__main__':
  fire.Fire(Run)
