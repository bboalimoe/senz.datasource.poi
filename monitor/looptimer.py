__author__ = 'wzf'

from threading import Timer

class LoopTimer(object):
    def __init__(self, interval, payload, argDict={}, alarm=None):
        self.interval = interval
        self.payload = payload
        self.argDict = argDict
        self.alarm = alarm

    def loop(self):
        try:
            self.payload(**self.argDict)

            self.start()
        except Exception as e:
            if self.alarm:
                self.alarm()
            return

    def start(self):
        t = Timer(self.interval, self.loop())
        t.start()

def f(a, b=None):
    raise Exception("hello")

if __name__ == '__main__':
    timer = LoopTimer(1, f, {"a": 1})
    timer.start()

