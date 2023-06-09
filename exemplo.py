import http.client as request
import asyncio
from time import perf_counter
import json

def timer(func):
    async def wrapper(*args, kwargs):
        start = perf_counter()
        res = await func(*args, **kwargs)
        end = perf_counter - start
        print(f'{func.__name__}executou em {end:0.2f} segundos')
        return res
    return wrapper

def image_urls():
    conn = request.HTTPSConnection('jsonplaceholder.typicode.com')
    conn.request('GET', '/photos')
    data = conn.getresponse().read()
    images = json.loads(data)
    for img in images:
        conn = request.HTTPSConnection(img['url'].split('/')[2])
        caminho = img['url'].split('/', 3)[-1]
        yield conn, caminho


async def dowload_and_transform(conn, path):
    print(f'obtendo imagem: {path}')
    conn.request('GET', f'/{path}')
    image = conn.getresponse().read()
    return image


async def dowload_images():
    tasks = []
    k = 0
    for conn, path in image_urls():
        task = asyncio.ensure_future(dowload_and_transform(conn, path))
        tasks.append(task)
        k += 1
        if k == 10: break

    image_data_list = await asyncio.gather(*tasks)

    for i, img_data in enumerate(image_data_list):
        with open(f'imagens/image_{i}', 'wb') as f:
            f.write(img_data)


asyncio.run(dowload_images())
