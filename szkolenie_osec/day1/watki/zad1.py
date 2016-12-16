from threading import Thread
# from multiprocessing import Process as Thread


def calculate():
    length = 0
    exp = 2
    while length < 4000:
        number = 2**exp
        length = len(str(number))
        exp += 1
    print(exp)

for _ in range(4):
    Thread(target=calculate).start()

# calculate()
