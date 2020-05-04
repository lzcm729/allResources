# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 20:14:24 2020

@author: Qianzhen
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from more_itertools import split_after

class NotbasicResources(Exception):
    pass

#获取网页text格式
def get_htmlText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'utf-8'
        text = r.text
    except:
        print('Error')
        
    return(text)
    
    
#根据主页建立所有物品名的汇总列表    
def fill_inventoryList(text):
    lt = []
    inventoryList = []
    soup = BeautifulSoup(text, 'html.parser')
    lt = soup.find('div', class_='inventory').find_all('img')
    
    for item in lt:
        inventoryList.append(item.attrs['alt'])
        
    del inventoryList[0:4]   #删除头四个无用数据
    
    return inventoryList
                       

#根据物品的汇总列表查询单独页面，将单独的物品页面与物品名建立键值对，并保存为本地文件
def saveHtmlText(inventoryList, fpath):
    local_sum_text = []
    for inventory in inventoryList:
        item_page = 'https://wiki.factorio.com/{}'.format(inventory.replace(' ', '_'))
        try:
            item_page_text = get_htmlText(item_page)
            local_sum_text.append(item_page_text)
            print('Acquired ' + inventory)
        except:
            print('Acquisition Failure')
            local_sum_text.append('Acquisition Failure')
            continue
        
    item_webtxt_data = dict(zip(inventoryList, local_sum_text))
    
    with open(fpath, 'w+') as f:
        f.write(json.dumps(item_webtxt_data))
            
    return 0
    
    
#读取本地json文件
def read_local_json(jfile):
    with open(jfile, 'r') as f:
        data = json.load(f)
        
    return(data)


#记录问题
def log(lt):
    with open(r'C:\Users\Qianzhen\OneDrive\Game Related\Factorio\log.json', 'w+') as f:
        f.write(json.dumps(lt, indent=1))
            
    return 0


#联网下载数据并保存
def download_file(fpath):
    mainpage = 'https://wiki.factorio.com/Main_Page'
    webtext = get_htmlText(mainpage)
    inventoryList = fill_inventoryList(webtext)
    
    zh_mainpage = 'https://wiki.factorio.com/Main_Page/zh'
    zh_webtext = get_htmlText(zh_mainpage)
    zh_inventoryList = fill_inventoryList(zh_webtext)
    
    saveHtmlText(inventoryList, fpath)
    
    return 0
    

#解析配方信息
def parse_recipe(t, exceptions_list):
    mode = 'Normal mode'
    k, v = t
    
    t_num_list = []
    
    preMaterial_list = []
    preMaterial_number = []
    
    #前提判断
    if k in exceptions_list[0]:                 #排除初级资源
        preMaterial_list.append(None)
        preMaterial_number.append(None)
    elif k in exceptions_list[1]:               #排除蓝图工具
        preMaterial_list.append('User')
        preMaterial_number.append(None)
    elif k in exceptions_list[2]:               #排除内容桶
        preMaterial_list.append(k[:-7])
        preMaterial_number.append(None)
    elif k == 'Empty barrel':                   #排除空桶
        preMaterial_list.append('Time')
        preMaterial_list.append('Steel plate')
        preMaterial_number.append('1')
        preMaterial_number.append('1')
    elif k == 'Space science pack':             #排除太空科技包
        preMaterial_list.append('Time')
        preMaterial_list.append('Rocket part')
        preMaterial_list.append('Satellite')
        preMaterial_number.append('0')
        preMaterial_number.append('100')
        preMaterial_number.append('1')
        
    else:   #开始解析网页
        soup = BeautifulSoup(v, 'html.parser')                              
        try:    
            #定位到不同mode
            area = soup.find('div', title = re.compile(mode))
            #配方的需求物种
            preMaterial_list = area.find('td', class_='infobox-vrow-value').find_all('a', title=True)
            #配方需求物种的数量
            t_num_list = area.find('td', class_='infobox-vrow-value').find_all('div', class_='factorio-icon-text')
        except AttributeError:          #非普通页面(oil和Solid fuel)
            if k == 'Solid fuel':       #Solid fuel
                area = soup.find('table', class_='wikitable')
                
                preMaterial_list = area.find_all('a', title=True)
                preMaterial_number = list(map(lambda x: x.next_sibling, preMaterial_list))
                
                preMaterial_list = list(map(lambda x: x.attrs['title'], preMaterial_list))
                preMaterial_number = list(map(lambda x: float(x.contents[0]), preMaterial_number))
                
                
#                process = ['From {}'.format()]
                
                recipe = list(zip(preMaterial_list, preMaterial_number))
                print(recipe)
                
            else:                       #oil
                
                print('Need operation \t' + k)
        except:
            print('Parse Failure \t\t' + k)                        
        else:
            preMaterial_list = list(map(lambda x: x.attrs['title'], preMaterial_list[:-1]))
            
            for num in t_num_list[:-1]:
                try:
                    preMaterial_number.append(float(num.contents[0]))
                except ValueError:  #1k转换成1000
                    if 'k' == num.contents[0][-1]:
                        preMaterial_number.append(float(num.contents[0][:-1]+'000'))
                    else:
                        print('NumberError')
                        
    recipe = dict(zip(preMaterial_list, preMaterial_number))
    recipe_with_name = {k:recipe}
    
    return(recipe_with_name)   


    
def main():
    file_location = r'C:\Users\Qianzhen\OneDrive\Game Related\Factorio\item_webtxt_data.json'
    
    basicResources = ['Wood', 'Coal', 'Stone', 'Iron ore', 'Copper ore', 'Uranium ore', 'Raw fish', 'Crude oil', 'Water', 'Steam']
    bluePrintTool = ['Blueprint', 'Deconstruction planner', 'Upgrade planner', 'Blueprint book']
    substantial_barrel = ['Crude oil barrel', 'Heavy oil barrel', 'Light oil barrel', 'Lubricant barrel', 'Petroleum gas barrel', 'Sulfuric acid barrel', 'Water barrel']
    muti_process = ['Heavy oil', 'Light oil', 'Petroleum gas', 'Solid fuel']
    
    exceptions_list = [basicResources, bluePrintTool, substantial_barrel, muti_process]
    
#    download_file(file_location)
    item_webtxt_data = read_local_json(file_location)
    
    all_recipe = []
    for data in item_webtxt_data.items():
        all_recipe.append(parse_recipe(data, exceptions_list))
        
    log(all_recipe)
    
    return 0


if __name__ == "__main__":
    # execute only if run as a script
    main()
