import time


class mesure_time:
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
            return results
        return decorate

    def summary(self):
        print('Nazwa\tIlosc wywolan\tSredni czas')
        for func, (count, avg_time) in self.called_methods.items():
            print ("{:10}\t{:5}\t{:10}".format(func.__name__, count, avg_time))



timeit = mesure_time()


@timeit
def foo():
    print('foo')
    time.sleep(1)


@timeit
def hehehe():
    print('heheheeh')
    time.sleep(2)


if __name__ == '__main__':
    foo()
    hehehe()
    foo()

    timeit.summary()
