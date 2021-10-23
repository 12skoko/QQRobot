import time
import requests
import interval
import getSessionKey
from msg_12skoko import msg_12skoko
from sandMsg import sandMsg


def processMsg(cbdata):
    if cbdata['type'] == 'FriendMessage' and cbdata['sender']['id'] == 1458987208:
        msg_12skoko(cbdata['messageChain'], key)


if __name__ == '__main__':

    interval = interval.interval()
    key = getSessionKey.SessionKey()
    se = requests.session()
    while (1):
        req = se.get(key.posturl+'/fetchMessage?sessionKey=' + key.getSessionKey() + '&count=1')

        if not (req.json()['msg'] == '' and req.json()['data'] == []):
            interval.update()
            print('receive:'+str(req.json()['data'][0]))
            try:
                processMsg(req.json()['data'][0])
            except Exception as e :
                print(e)
                print('处理错误')
                sandMsg(str(req.json()), key.admin, 'FriendMessage', key)
                sandMsg(str(e), key.admin, 'FriendMessage', key)

        time.sleep(interval.getIntervalTime())
