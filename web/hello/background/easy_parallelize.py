from multiprocessing.dummy import Pool
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp
import concurrent
import time
import random

max_pool_size = 8
"""
parallely work toolkit
"""


def easy_parallelize(func, data, pool_size=None):
    # make number of workers fit size of input data, if not specified otherwise
    if pool_size is None or pool_size < 1:
        pool = Pool(processes=max_pool_size)
    else:
        pool = Pool(processes=pool_size)

    results = pool.map(func, data)

    # cleaning out None results
    cleaned = filter(None, results)

    pool.close()
    pool.join()

    return cleaned, "ok"


def easy_ThreadSubmit(func, data, pool_size=None):
    res = []
    if pool_size is None or pool_size < 1:
        pool = ThreadPoolExecutor(max_workers=max_pool_size)
    else:
        pool = ThreadPoolExecutor(max_workers=pool_size)
    futures = {pool.submit(func, one): one for one in data}
    # futures = {}
    # for one in data:
    #     random.seed()
    #     time.sleep(random.random()*4)
    #     futures.get(pool.submit(func, one))

    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
            res.append(result)
        except Exception:
            pass

    return res


def easy_ThreadMax(func, data, pool_size=None):
    res = []
    if pool_size is None or pool_size < 1:
        pool = ThreadPoolExecutor(max_workers=max_pool_size)
    else:
        pool = ThreadPoolExecutor(max_workers=pool_size)
    results = pool.map(func, data)
    for result in results:
        res.append(result.result())

    return res


def easy_SerialWork(func, lock, running, filepath):
    random.seed()
    time.sleep(random.random() * 4)

    lock.acquire()
    try:
        func(filepath)
        print('Current processing', running)
    except Exception:
        print('Current wrong processing', running)
        print(Exception)
    finally:
        lock.release()


def easy_SerialStart(func, datas, datalength):
    lock = mp.Lock()

    for i in range(datalength):
        mp.Process(target=easy_SerialWork, args=(func, lock, i, datas[i])).start()
