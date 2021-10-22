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
        req = se.get('http://127.0.0.1:8080/fetchMessage?sessionKey=' + key.getSessionKey() + '&count=1')

        if not (req.json()['msg'] == '' and req.json()['data'] == []):
            interval.update()
            print(req.json()['data'][0])
            try:
                processMsg(req.json()['data'][0])
            except:
                print('处理错误')
                sandMsg('申请失败', 1458987208, 'FriendMessage', key)

        time.sleep(interval.getIntervalTime())
