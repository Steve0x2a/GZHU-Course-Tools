from sample import jw,get_course

username = '1719500024'
password = 'zhanyi051414'
jwlogin = jw.login(username,password)
#jwlogin.main()
get = get_course.course(username)
get.save_courses()
