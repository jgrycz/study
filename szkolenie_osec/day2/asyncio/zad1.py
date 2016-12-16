import os.path
import asyncio
import aiohttp


img = ['http://eloblog.pl/wp-content/uploads/2015/10/Monkey-selfie.jpg',
       "http://digitalcamerapolska.pl/imgcache/images/6/8/8/c3JjPS9pbWFnZXMvNi84LzgvMTI2ODgtamFrX3JvYmljX29zdHJlX3pkamVjaWFfMDEuanBnJnc9NzUw_srcb0198834f9a076f76d3c0da7e2f58ec7.jpg",
       "http://digitalcamerapolska.pl/imgcache/images/6/8/9/c3JjPS9pbWFnZXMvNi84LzkvMTI2ODktamFrX3JvYmljX29zdHJlX3pkamVjaWFfMDIuanBnJmNyb3BzY2FsZT0xJng9MCZ5PTAmdz0xMjAwJmg9ODAwJncxPTc1MCZoMT01MDA=_srcee404e59bfd92df8706f75184d229e1d.jpg"]


async def download(url, target_name):
    target_path = 'imgs'
    with aiohttp.ClientSession() as session:
        print("Donwloading: {}".format(target_name))
        async with session.get(url) as resp:
            if resp.status == 200:
                image = await resp.read()
                with open(os.path.join(target_path, target_name), "wb") as f:
                    f.write(image)


async def main():
    name_template = "malapa{}.jpg"
    loop = asyncio.get_event_loop()
    # await asyncio.gather(download(url, name_template.format(num)) for num, url in enumerate(img*3))
    await asyncio.gather(download(img[0], name_template.format(0)),
                         download(img[1], name_template.format(1)))

asyncio.get_event_loop().run_until_complete(main())
