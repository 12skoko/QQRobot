import time


class interval():
    def __init__(self):
        self._interval = {1: 10, 2: 1, 3: 0.2}
        self._lastMsgTime = [0, 0, 0, 0, 0]

    def getIntervalTime(self):
        msgTime = int(time.time())

        if msgTime - self._lastMsgTime[4] > 600:
            return self._interval[1]

        elif msgTime - self._lastMsgTime[0] < 10:
            return self._interval[3]

        else:
            return self._interval[2]

    def update(self):

        for i in range(4):
            self._lastMsgTime[i] = self._lastMsgTime[i + 1]

        self._lastMsgTime[4] = int(time.time())
