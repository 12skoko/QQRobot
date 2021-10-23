import requests
import time
import yaml


class SessionKey():
    def __init__(self):
        with open('config.yaml', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            self.posturl = data['posturl']
            self._verifyKey = data['verifyKey']
            self._robotQQ = data['robotQQ']
            self.admin=data['admin']
        self._Timestamp = int(time.time())
        self._sessionKey = self._initSessionKey()

    def _initSessionKey(self):
        se = requests.session()

        data = {"verifyKey": self._verifyKey}

        rep = se.post(url=self.posturl + '/verify', json=data)

        redict = rep.json()

        sessionKey = redict['session']

        data = {
            "sessionKey": sessionKey,
            "qq": self._robotQQ
        }

        rep = se.post(url=self.posturl + '/bind', json=data)

        assert rep.json()['code'] == 0 and rep.json()['msg'] == 'success'

        return sessionKey

    def _keyIsValid(self):
        Timestamp_temp = int(time.time())
        if Timestamp_temp - self._Timestamp > 1800:
            return -1
        data = {
            "sessionKey": self._sessionKey,
            "qq": self._robotQQ
        }
        rep = requests.post(url=self.posturl + '/bind', json=data)
        if rep.json()['code'] == 0 and rep.json()['msg'] == 'success':
            del rep
            return 0
        else:
            del rep
            return -1

    def getSessionKey(self, display=0):
        if self._keyIsValid() == 0:
            if display != 0:
                print(self._sessionKey)
            return self._sessionKey
        else:
            self._Timestamp = int(time.time())
            self._sessionKey = self._initSessionKey()
            if display != 0:
                print(self._sessionKey)
            return self._sessionKey
