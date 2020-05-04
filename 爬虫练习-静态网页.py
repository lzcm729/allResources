# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 22:05:45 2020

@author: Qianzhen
"""

import requests
import re
from bs4 import BeautifulSoup
import bs4

def get_htmlText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'utf-8'
        text = r.text
    except:
        print('Error')
        
    return(text)


def fill_univList(ulist, uInfo, text):
    soup = BeautifulSoup(text, 'html.parser')
    for tr in soup.find('tbody').find_all('tr'):    #tr对应每一所学校
        uInfo.append(tr)                        
            
    uInfo = list(map(lambda x: x.find_all('td'), uInfo))#拆分tr到td
    for item in uInfo:
        ulist.append(list(map(lambda x: x.string, [item[0], item[1], item[2], item[3]])))
        
    return 0

def print_univList(ulist, num):
    scgs = '{0:^5}{1:{4}^10}{2:{4}^6}{3:^6}'
    blk = chr(12288)
    print(scgs.format('排名','名字','地区','分数', blk))
    for i in range(num):
        print(scgs.format(ulist[i][0], ulist[i][1], ulist[i][2], ulist[i][3], blk))


def main():
    uInfo = []
    ulist = []
    url = 'http://zuihaodaxue.cn/zuihaodaxuepaiming2016.html'
    text = get_htmlText(url)
    fill_univList(ulist, uInfo, text)
    print_univList(ulist, 20)
    
    
main()