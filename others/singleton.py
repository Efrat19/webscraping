import threading
from time import sleep

lock = threading.Lock()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        sleep(1)
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        "__call__ from Singleton"
        return cls._instances[cls]


class SingletonNotThreadSafe(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        sleep(10)
        if cls not in cls._instances:
            if cls not in cls._instances:
                cls._instances[cls] = super(SingletonNotThreadSafe, cls).__call__(*args, **kwargs)
        print
        "__call__ from SingletonNotThreadSafe"
        return cls._instances[cls]


class FetcherOptions(object):
    __metaclass__ = Singleton

    def __init__(self):
        print
        "starting__init__"
        self.prop1 = self._calculate_prop_1()
        self.prop2 = self._calculate_prop_2()

    def _calculate_prop_1(self):
        return 1

    def _calculate_prop_2(self):
        return 2

    def get_prop_1(self):
        return self.prop1

    def __repr__(self):
        return "{}\n{}\n ".format(self.__metaclass__, self.__dict__)


ids_list = []


def create_fetcher_options():
    print(id(FetcherOptions()))


process_list = []
thread_num = 1
for i in range(thread_num):
    t = threading.Thread(target=create_fetcher_options, args=())
    process_list.append(t)

for i in range(thread_num):
    process_list[i].start()

print(FetcherOptions())
# print id(FetcherOptions())
