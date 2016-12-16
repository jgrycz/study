import requests
import os.path
import asyncio
import shutil


imgs = ['http://eloblog.pl/wp-content/uploads/2015/10/Monkey-selfie.jpg',
        "http://digitalcamerapolska.pl/imgcache/images/6/8/8/c3JjPS9pbWFnZXMvNi84LzgvMTI2ODgtamFrX3JvYmljX29zdHJlX3pkamVjaWFfMDEuanBnJnc9NzUw_srcb0198834f9a076f76d3c0da7e2f58ec7.jpg",
        "http://digitalcamerapolska.pl/imgcache/images/6/8/9/c3JjPS9pbWFnZXMvNi84LzkvMTI2ODktamFrX3JvYmljX29zdHJlX3pkamVjaWFfMDIuanBnJmNyb3BzY2FsZT0xJng9MCZ5PTAmdz0xMjAwJmg9ODAwJncxPTc1MCZoMT01MDA=_srcee404e59bfd92df8706f75184d229e1d.jpg"]
target_path = "imgs"
name_template = "malapa{}.jpg"


async def get_photo(loop, url, target_name):
    print('Requesting {}'.format(target_name))
    return await loop.run_in_executor(None, lambda: requests.get(url, stream=True))
    #return requests.get(url, stream=True)


def save_photo(resp, target_name):
    print('Downloading {}'.format(target_name))
    if resp.status_code == 200:
        with open(os.path.join(target_path, target_name), 'wb') as f:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, f)


async def download_and_save(loop, url, target_name):
    resp = await get_photo(loop, url, target_name)
    await loop.run_in_executor(None, save_photo, resp, target_name)


async def main(loop):
    await asyncio.gather(*[download_and_save(loop, url, name_template.format(num)) for num, url in enumerate(imgs*4)])


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
