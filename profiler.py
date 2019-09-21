"""
This class is used to time profile

Without Using Redis-Cache
Average time taken over 1001 different words 59.1797 ms
Average time taken over 2001 different words 61.4683 ms
Average time taken over 3001 different words 64.1792 ms

With Use of Redis-Cache
Average time taken over 5001 different words 0.08147640228271484 ms
"""

import os

from src.Server import Server
from iomanagers.redis_manager import RedisManager

import time
import requests
import pandas as pd
import numpy as np


#words file
PATH = "https://raw.github.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt"
server = Server(connect_to_db=False)
redis_mgr = RedisManager("localhost", "6379", 0)

class profiler():
    def __init__(self, file):
        self.wordsfile = file
        if 'words.txt' not in os.listdir(os.getcwd()):
            response = requests.get(self.wordsfile, allow_redirects=True)
            print(response.headers.get('content-type'))
            with open('words.txt', 'wb') as f:
                f.write(response.content)

    def _profile(self):
        """ No Redis query used  """
        times = []
        with open("words.txt", 'r') as f:
            word = f.readline()
            cnt = 1
            while word and cnt <= 3000:
                #time it
                s = time.time()
                search_result = server.search(word)
                e = time.time()
                times.append((e-s)*1000)
                print(word)
                word = f.readline()
                cnt += 1
        #calcualate the average
        print(f"Average time taken over {cnt} different words {np.mean(times)} ms")

    def _profileWithRedis(self):
        """ Profiling with Redis  """
        times = []
        with open("words.txt", 'r') as f:
            word = f.readline()
            cnt = 1
            while word and cnt <= 5000:
                #time it
                s = time.time()
                search_result = redis_mgr.get_search_results(word)

                if not search_result :
                    search_result = server.search(word)
                    redis_mgr.cache_search_results(word, search_result)
                e = time.time()
                times.append((e-s)*1000)
                print(word)
                word = f.readline()
                cnt += 1
        #calculate the average
        print(f"Average time taken over {cnt} different words {np.mean(times)} ms")


if __name__ == "__main__":
    prof = profiler(PATH)
    prof._profileWithRedis()


