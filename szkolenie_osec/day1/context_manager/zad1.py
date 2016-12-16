from contextlib import contextmanager


class MyOwnException(Exception):
    pass


@contextmanager
def throws(exception):
    try:
        yield
    except exception as e:
        print("Kod rzucil wyjatek {}".format(e))
    except Exception as e:
        print e
        raise MyOwnException('Cos sie stalo dziwnego')
    else:
        print('nie bylo wyjatku: {}'.format(exception.__name__))


if __name__ == '__main__':
    with throws(ZeroDivisionError):
        # 1 > 0
        opeln('dupa')
