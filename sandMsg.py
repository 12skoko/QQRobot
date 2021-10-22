import requests
# import getSessionKey

def sandMsg(text,target,type,key,display=1):

    data = {
        "sessionKey": key.getSessionKey(),
        "target": target,
        "messageChain": [
            {"type": "Plain", "text": text}
        ]
    }
    if display!=0:
        print(data)
    rep = requests.post(url='http://127.0.0.1:8080/send'+type, json=data)
    assert rep.json()['code'] == 0 and rep.json()['msg'] == 'success'
    del rep