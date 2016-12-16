from Queue import Queue
import threading as t
import requests
import os.path
import shutil

target_path = 'imgs'
img = ['http://eloblog.pl/wp-content/uploads/2015/10/Monkey-selfie.jpg',
       "http://digitalcamerapolska.pl/imgcache/images/6/8/8/c3JjPS9pbWFnZXMvNi84LzgvMTI2ODgtamFrX3JvYmljX29zdHJlX3pkamVjaWFfMDEuanBnJnc9NzUw_srcb0198834f9a076f76d3c0da7e2f58ec7.jpg",
       "http://digitalcamerapolska.pl/imgcache/images/6/8/9/c3JjPS9pbWFnZXMvNi84LzkvMTI2ODktamFrX3JvYmljX29zdHJlX3pkamVjaWFfMDIuanBnJmNyb3BzY2FsZT0xJng9MCZ5PTAmdz0xMjAwJmg9ODAwJncxPTc1MCZoMT01MDA=_srcee404e59bfd92df8706f75184d229e1d.jpg"]

downloading_queue = Queue()
imgs_queue = Queue()

for i, img in enumerate(img*4):
    imgs_queue.put(('malpa{}.jpg'.format(i), img,))


def get_photo(downloading_queue, imgs_queue):
    while not imgs_queue.empty():
        target_name, url = imgs_queue.get()
        print 'Requesting {}'.format(target_name)
        r = requests.get(url, stream=True)
        downloading_queue.put((r, target_name,))


def save_photo(downloading_queue, imgs_queue):
    while not (imgs_queue.empty() and downloading_queue.empty()):
        r, target_name = downloading_queue.get()
        print 'Downloading {}'.format(target_name)
        if r.status_code == 200:
            with open(os.path.join(target_path, target_name), 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

t.Thread(target=get_photo, args=(downloading_queue, imgs_queue,)).start()
t.Thread(target=get_photo, args=(downloading_queue, imgs_queue,)).start()
t.Thread(target=save_photo, args=(downloading_queue, imgs_queue,)).start()
t.Thread(target=save_photo, args=(downloading_queue, imgs_queue,)).start()

for th in t.enumerate():
    if not t.current_thread():
        th.join()
