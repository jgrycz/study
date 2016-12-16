def supress_exception(*exceptions):
    def wrap(f):
        def decorate(*args, **kwargs):
            try:
                results = f(*args, **kwargs)
                return results
            except exceptions:
                pass
        return decorate
    return wrap


@supress_exception(ZeroDivisionError, IOError)
def fooo():
    # raise ZeroDivisionError
    # raise IOError
    raise Exception
    return 'heehh'


if __name__ == '__main__':
    print fooo()
