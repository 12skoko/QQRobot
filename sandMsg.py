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
        print('sand:'+str(data))
    rep = requests.post(url=key.posturl+'/send'+type, json=data)
    assert rep.json()['code'] == 0 and rep.json()['msg'] == 'success'
    del rep