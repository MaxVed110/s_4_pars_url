# Задание №8
# Напишите программу, которая будет скачивать страницы из списка URL-адресов и сохранять их в отдельные файлы на
# диске. В списке может быть несколько сотен URL-адресов. При решении задачи нужно использовать многопоточность,
# многопроцессорность и асинхронность. Представьте три варианта решения.
import requests
import time
import os
import threading
import asyncio
import aiohttp
from multiprocessing import Process


def download(url: str, folder):
    response = requests.get(url)
    file_name = url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
    with open(folder + '/' + file_name, 'w', encoding='utf-8') as f:
        f.write(response.text)


def thread_load_data_url(path_file_list: str):
    """thread: 4.539388656616211"""
    start_time = time.time()
    folder = 'threading_data'
    os.mkdir(folder)
    threads = []
    with open(path_file_list, 'r') as f:
        list_url = f.readlines()
    list_url = [line.rstrip() for line in list_url]
    for url in list_url:
        thread = threading.Thread(target=download, args=[url, folder])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    finish_time = time.time() - start_time
    print(f'thread: {finish_time}')


def multiprocessing_load_data_url(path_file_list: str):
    """multiprocessing: 3.8842251300811768"""
    start_time = time.time()
    folder = 'multiprocessing_data'
    os.mkdir(folder)
    processes = []
    with open(path_file_list, 'r') as f:
        list_url = f.readlines()
    list_url = [line.rstrip() for line in list_url]
    for url in list_url:
        process = Process(target=download, args=(url, folder))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    finish_time = time.time() - start_time
    print(f'multiprocessing: {finish_time}')


async def download_as(url: str, folder):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            file_name = url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
        with open(folder + '/' + file_name, 'w', encoding='utf-8') as f:
            f.write(text)


async def async_load_data_url(path_file_list: str):
    """async: 26.459713220596313"""
    start_time = time.time()
    folder = 'async_data'
    os.mkdir(folder)
    tasks = []
    with open(path_file_list, 'r') as f:
        list_url = f.readlines()
    list_url = [line.rstrip() for line in list_url]
    for url in list_url:
        task = asyncio.ensure_future(download_as(url, folder))
        tasks.append(task)
    await asyncio.gather(*tasks)

    finish_time = time.time() - start_time
    print(f'async: {finish_time}')


if __name__ == '__main__':
    # thread_load_data_url('list_url.txt')
    # multiprocessing_load_data_url('list_url.txt')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_load_data_url('list_url.txt'))
