from threading import Thread
from time import sleep


class MonThread(Thread):

    def __init__(self,id):
        super().__init__()
        self.__id = id


    def run(self):
        for i in range(100):
            print(self.__id)




T1 = MonThread(1)
T2 = MonThread(2)
T1.start()
T2.start()

