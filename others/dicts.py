import threading

lock = threading.Lock()


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FetcherOptions(object):
    __metaclass__ = SingletonMeta

    def __init__(self):
        self.counter = 0
        self._example = "example"

        self._options_map = {
            'knowledge_articles_enabled': "yeah yeah!",
            'back_up_files': 2,
            'max_files': 3,
            'excluded_tables': [],
            'FETCHER_POOL_SIZE': 4,
        }

    @property
    def example(self):
        print
        self.counter
        self.counter += 1
        return self._example

    @property
    def knowledge_articles_enabled(self):
        self.counter += 1
        print
        self.counter
        return self._options_map["knowledge_articles_enabled"]

    @property
    def attr(self, attribute):
        return self._options_map[attribute]


f = FetcherOptions()

for i in range(10):
    print
    FetcherOptions().attr('back_up_files')
