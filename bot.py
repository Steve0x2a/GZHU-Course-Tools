from run import wxbot
from wxpy import *


bot = Bot()
run = wxbot()
my_friend = ensure_one(bot.search('0x2a'))



# 使用图灵机器人自动与指定好友聊天
@bot.register(my_friend)
def reply_my_friend(msg):
    raw = msg.text.split()
    if raw[0] == 'help':
        msg.reply_msg('1. 首先输入\'login 学号 密码\' 登录\
                        \n2. 然后输入\'select 学号 密码 选课编号\' 开始选课\
                        \n3. 可以输入\'refresh学号\' 确定cookie是否存在\
                        \n4. 请不要在抢课开始后进行刷新cookie操作\
                        \n5. cookie 可能失效 输入\'refresh 账号 密码\' 刷新cookie\
                        \n6.输入\'show 学号 密码 查看当前已选课程')
    elif raw[0] == 'select':
        res = run.wx_select(raw[1],raw[2],raw[3])     
        msg.reply_msg(res)
    elif raw[0] == 'refresh':
        res = run.wx_refresh(raw[1],raw[2])
        msg.reply_msg(res)
    elif raw[0] == 'login':
        res = run.wx_login(raw[1],raw[2])
        msg.reply_msg(res)
    elif raw[0] == 'show':
        res = run.wx_show(raw[1],raw[2])
        msg.reply_msg(res)        
    else:
        msg.reply_msg('指令错误! 输入help查看使用指南')


embed()

