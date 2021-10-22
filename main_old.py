from flask import Flask, request
import getSessionKey
import requests
import re
import json
import csv
import out

def sandMsg(text,target,type):

    data = {
        "sessionKey": key.getSessionKey(),
        "target": target,
        "messageChain": [
            {"type": "Plain", "text": text}
        ]
    }
    rep = requests.post(url='http://127.0.0.1:8080/send'+type, json=data)
    assert rep.json()['code'] == 0 and rep.json()['msg'] == 'success'
    del rep



def skoko12_msg_Forward(text):
    re_com=re.compile('"type": "Image", "imageId": "(.*?)", "url": "(.*?)"')
    urllist=re.findall(re_com,json.dumps(text))
    with open('imageurl.csv','a',newline='') as f:
        writer=csv.writer(f)
        for i in urllist:
            writer.writerow(i)
    sandMsg('已保存'+str(len(urllist))+'张图片', 1458987208, 'FriendMessage')

def skoko12_msg_Plain(text):
    if text=='出校':
        try:
            # out.out('info_zl')
            sandMsg('申请成功', 1458987208, 'FriendMessage')
        except:
            sandMsg('申请失败', 1458987208, 'FriendMessage')


def skoko12_msg(messageChain):
    for message in messageChain:
        if message['type']=='Source':
            pass
        if message['type']=='Forward':
            skoko12_msg_Forward(message)
        elif message['type']=='Plain':
            skoko12_msg_Plain(message['text'])





app = Flask(__name__)

@app.route('/qqrobot', methods=['POST'])
def qqrobot():
    # req_str = request.form[0:int(request.cont)]
    # req_data = json.loads(req_str, encoding='utf-8')

    cbdata = request.json()

    print(cbdata)
    print(key.getSessionKey())
    if cbdata['type']=='FriendMessage' and cbdata['sender']['id']==1458987208 :

        rpostdata=skoko12_msg(cbdata['messageChain'])

        req = requests.post(url='http://127.0.0.1:8080/sendFriendMessage', json=rpostdata)

        print(req.text)

        del req

    return '200'

if __name__ == '__main__':
    key = getSessionKey.SessionKey()
    app.run(host='0.0.0.0', port=5000, debug=False)
#    - 'localhost:5000/qqrobot'
#{'type': 'FriendMessage', 'messageChain': [{'type': 'Source', 'id': 58517, 'time': 1634541489}, {'type': 'Plain', 'text': '一'}], 'sender': {'id': 1458987208, 'nickname': '12skoko', 'remark': '12skoko'}}