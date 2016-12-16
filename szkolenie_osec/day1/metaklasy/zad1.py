import time


class TimeIt:
    def __init__(self):
        self.called_methods = {}

    def __call__(self, f):
        def decorate(*args, **kwargs):
            start = time.time()
            results = f(*args, **kwargs)
            stop = time.time()

            if f not in self.called_methods:
                self.called_methods[f] = (1, stop-start)
            else:
                count, avg_time = self.called_methods[f]
                self.called_methods[f] = (count + 1, (avg_time + (stop - start)) / 2)
            print('Duration time {}: {}'.format(f.__qualname__, stop-start))
            return results
        return decorate

    def summary(self):
        print('Nazwa\tIlosc wywolan\tSredni czas')
        for func, (count, avg_time) in self.called_methods.items():
            print ("{:10}\t{:5}\t{:10}".format(func.__qualname__, count, avg_time))


timeit = TimeIt()


class LoggingMeta(type):
    def __new__(cls, classname, parents, attrs):
        for attr in attrs.keys():
            if not attr.startswith('__'):
                attrs[attr] = timeit(attrs[attr])
        return super().__new__(cls, classname, parents, attrs)


class Hehehe(metaclass=LoggingMeta):
    def __init__(self):
        pass

    def hehehe(self):
        pass

    def _hoho(self):
        pass


class Hehehe2(metaclass=LoggingMeta):
    def __init__(self):
        pass

    def hehehe(self):
        pass

    def _hoho(self):
        pass



if __name__ == '__main__':
    he = Hehehe()
    he.hehehe()
    he._hoho()

    he2 = Hehehe2()
    he2.hehehe()
    he2._hoho()

    timeit.summary()
