import os
import httplib2
import requests
import time
import threading
import asyncio
import aiohttp
from multiprocessing import Process
from bs4 import BeautifulSoup
from sys import argv


def threading_method(path_file_list, list_url):
    start_time = time.time()
    folder = 'threading_img'
    if not os.path.isdir(folder):
        os.mkdir(folder)
    threads = []
    urls = list_url
    if urls is None:
        with open(path_file_list, 'r') as f:
            urls = f.readlines()
        urls = [line.rstrip() for line in urls]
    for url in urls:
        thread = threading.Thread(target=download_img_for_thr_and_multi, args=[url, folder])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    finish_time = time.time() - start_time
    print(f'Программа завершила работу за: {round(finish_time, 5)} сек.')


def multiproc_method(path_file_list, list_url):
    start_time = time.time()
    folder = 'multiproc_img'
    if not os.path.isdir(folder):
        os.mkdir(folder)
    processes = []
    urls = list_url
    if urls is None:
        with open(path_file_list, 'r') as f:
            urls = f.readlines()
        urls = [line.rstrip() for line in urls]
    for url in urls:
        process = Process(target=download_img_for_thr_and_multi, args=(url, folder))
        processes.append(process)
        process.start()

    for proc in processes:
        proc.join()

    finish_time = time.time() - start_time
    print(f'Программа завершила работу за: {round(finish_time, 5)} сек.')


async def async_method(path_file_list, list_url):
    start_time = time.time()
    folder = 'async_img'
    if not os.path.isdir(folder):
        os.mkdir(folder)
    tasks = []
    urls = list_url
    if urls is None:
        with open(path_file_list, 'r') as f:
            urls = f.readlines()
        urls = [line.rstrip() for line in urls]
    for url in urls:
        task = asyncio.ensure_future(download_for_async(url, folder))
        tasks.append(task)
    await asyncio.gather(*tasks)

    finish_time = time.time() - start_time
    print(f'Программа завершила работу за: {round(finish_time, 5)} сек.')


def download_img_for_thr_and_multi(url, folder):
    http = httplib2.Http()
    resp, content = http.request(url)
    images = BeautifulSoup(content).findAll('img')
    image_links = []
    for image in images:
        try:
            image_links.append(image['src'])
        except KeyError:
            continue
    for img in image_links:
        if img.endswith('.jpg') or img.endswith('.png'):
            start_img = time.time()
            filename = img.split('/')[-1]
            response = requests.get(img, stream=True)
            with open(folder + '/' + filename, 'bw') as f:
                for chunk in response.iter_content(4096):
                    f.write(chunk)
            finish_img = time.time()
            print(f'Изображение {filename} загружено за {round(finish_img - start_img, 5)} сек.')


async def download_for_async(url, folder):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            resp = await response.text()
            images = BeautifulSoup(resp).findAll('img')
            image_links = []
            for image in images:
                try:
                    image_links.append(image['src'])
                except KeyError:
                    continue
            for img in image_links:
                if img.endswith('.jpg') or img.endswith('.png'):
                    start_img = time.time()
                    filename = img.split('/')[-1]
                    response = requests.get(img, stream=True)
                    with open(folder + '/' + filename, 'bw') as f:
                        for chunk in response.iter_content(4096):
                            f.write(chunk)
                    finish_img = time.time()
                    print(f'Изображение {filename} загружено за {round(finish_img - start_img, 5)} сек.')


def main(flag, path_file_list='list_url.txt', list_url = None):
    if flag == 't':
        threading_method(path_file_list, list_url)
    if flag == 'm':
        multiproc_method(path_file_list, list_url)
    if flag == 'a':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(async_method(path_file_list, list_url))


if __name__ == '__main__':
    main('t')
