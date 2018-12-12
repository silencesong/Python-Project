import requests
import itchat #这是一个用于微信回复的库
from itchat.content import *
import random


KEY = "11ce8a607b50469bab70d4664782b766"

# 向api发送请求
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
    'key'  : KEY,
    'info'  : msg,
    'userid' : 'pth-robot',
    }
    try:
        r=requests.post(apiUrl, data=data).json()
        text=r.get('text')
        url=r.get('url')#股票，油价，列车，图片的链接地址
        list = r.get('list') #含有菜谱，新闻资讯的链接地址的列表
        if list is not None:
            list_url = list[0]['detailurl']#从列表中提取地址
        else:
            list_url = list
        if url is None:
            if list_url is None:
                return text
            return "%s:%s" % (text, list_url)
        return "%s:%s" % (text, url)

    except:
        return

# 单人聊天
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = 'I received: ' + msg['Text']
    # 如果图灵Key出现问题，那么reply将会是None
    robots = ['——By机器人小白', '——By机器人小黑', '——By反正不是本人']
    reply = get_response(msg['Text']) + random.choice(robots)
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    return reply or defaultReply


#自动添加好友
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])# 该操作将自动将好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!',msg['RecommendInfo']['UserName'])


#群聊
@itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
def group_text_reply(msg):
    from_group = ''
    group = itchat.get_chatrooms(update=True)
    for g in group:
        #print(g['NickName'])#打印所有群名
        if g['NickName'] == '测试群': #换成自己群的名称
            from_group = g['UserName'] #获取群名对应的id
    if msg['FromUserName'] ==from_group:
        # 当然如果只想针对@我的人才回复，可以设置if msg['isAt']:
        if msg['isAt']:
            reply = get_response(msg['Text'])
            itchat.send('@%s: %s ' % (msg['ActualNickName'], reply), msg['FromUserName'])


# 保存图片或语音等
@itchat.msg_register([PICTURE,RECORDING,ATTACHMENT,VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])


# 为了让修改程序不用多次扫码,使用热启动
itchat.auto_login(hotReload=True)
itchat.run()


