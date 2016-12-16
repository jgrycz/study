import gevent
import gevent.monkey
from gevent import subprocess
gevent.monkey.patch_all()


tasks = ['zadania/hehe.py', 'zadania/hoho.py']


def run_task(task):
    proc = subprocess.Popen(task, stdout=subprocess.PIPE)
    while True:
        print(task)
        out = proc.stdout.read(32)
        if out == '':
            return
        print(out)
        gevent.sleep(2)


workers = [gevent.spawn(run_task, task) for task in tasks]
gevent.joinall(workers)

# run_task(tasks[0])
