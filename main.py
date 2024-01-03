# -*- coding: utf -8 -*-

import os
import re
import time
import itchat
import requests
from subprocess import Popen,PIPE
from itchat.content import INCOME_MSG

# 转发创米科技公众号视频到指定群聊
send_chatrooms = ["撸猫群"]

def download(url):
    r = requests.get(url)
    video_url = re.findall(r'<source src="(.*?)"', r.text)[0]
    filename = time.strftime("%Y%m%d-%H%M%S.mp4")
    Popen(f'ffmpeg -i "{video_url}" {filename} -y', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()
    return filename

def get_chatroom(nickname):
    chatrooms = itchat.get_chatrooms()
    for room in chatrooms:
        if room["NickName"] == nickname:
            return room["UserName"]

@itchat.msg_register(INCOME_MSG, isMpChat=True)
def msg_reply(msg):
    if msg["User"]["NickName"] == "创米数联":
        filename = download(msg.Url)
        for nickname in send_chatrooms:
            toUserName = get_chatroom(nickname)
            itchat.send_video(fileDir=filename, toUserName=toUserName)
        try:
            os.remove(filename)
        except:
            pass

if __name__ == "__main__":
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.run()
