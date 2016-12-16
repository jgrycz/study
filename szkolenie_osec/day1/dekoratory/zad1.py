import time


def mesure_time(f):
    def decorator(*args, **kwargs):
        start = time.time()
        results = f(*args, **kwargs)
        stop = time.time()
        print('Duration time: {}'.format(stop-start))
        return results
    return decorator


@mesure_time
def foo():
    time.sleep(1)


if __name__ == '__main__':
    foo()
