from time import sleep
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from selenium import webdriver
import concurrent.futures
import urllib.request  
import requests
import time

    
urls = ["https://namu.wiki/w/%EB%B6%84%EB%A5%98:%EC%A0%95%EC%88%98", 
        'https://namu.wiki/w/%EB%B6%84%EB%A5%98:%EC%88%98', 
        'https://namu.wiki/w/%EB%B6%84%EB%A5%98:%ED%95%9C%EA%B5%AD%20%EC%95%84%EC%9D%B4%EB%8F%8C', 
        'https://namu.wiki/w/%EB%B6%84%EB%A5%98:%EA%B1%B8%EA%B7%B8%EB%A3%B9']

    
limit = 20

def get_sublist_href(url: str):
    namu_link = []
    request = requests.get(url)
    sleep(1)
    
    parsed_html = BeautifulSoup(request.text, 'html.parser')
    a_element_tags = parsed_html.find_all('div', attrs={'class' : 'test'})
    for tag in a_element_tags:
        for link in tag.find_all('a'):
            namu_link.append(url + link['href'])
    
    namu_link = namu_link[:limit]
    print('Number of site: ', len(namu_link))
    return namu_link

def do_html_crawl(url: str):
    request = requests.get(url)
    sleep(1)
    parsed_html = BeautifulSoup(request.text, 'html.parser')
    return parsed_html

def do_process_with_thread_crawl(url: str):
    do_thread_crawl(get_sublist_href(url))
    
def do_thread_crawl(urls: list):
    thread_list = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        for url in urls:
            thread_list.append(executor.submit(do_html_crawl, url))
        for execution in concurrent.futures.as_completed(thread_list):
            execution.result()


if __name__ == "__main__":
    start_time = time.time()

    with Pool(processes=4) as pool:  
        pool.map(do_process_with_thread_crawl, urls)
        print("--- elapsed time %s seconds ---" % (time.time() - start_time))