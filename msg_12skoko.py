import re
import json
import csv
# import getSessionKey
from sandMsg import sandMsg


def _skoko12_msg_Forward(text,key):
    re_com=re.compile('"type": "Image", "imageId": "(.*?)", "url": "(.*?)"')
    urllist=re.findall(re_com,json.dumps(text))
    with open('imageurl.csv','a',newline='') as f:
        writer=csv.writer(f)
        for i in urllist:
            writer.writerow(i)
    sandMsg('已保存'+str(len(urllist))+'张图片', 1458987208, 'FriendMessage',key)

def _skoko12_msg_Plain(text,key):
    if text=='出校':
        try:
            # out.out('info_zl')
            sandMsg('申请成功', 1458987208, 'FriendMessage',key)
        except:
            sandMsg('申请失败', 1458987208, 'FriendMessage',key)


def msg_12skoko(messageChain,key):
    for message in messageChain:
        if message['type']=='Source':
            pass
        if message['type']=='Forward':
            _skoko12_msg_Forward(message,key)
        elif message['type']=='Plain':
            _skoko12_msg_Plain(message['text'],key)