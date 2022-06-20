# -*- coding: utf-8 -*-
"""
Created on Tue May 10 14:00:23 2022

@author: 陈纪程
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import time
import pandas as pd
import re

def card(number_indexs, card_text):
    #对剪贴板的numpy进行辅助性解析的函数
    cost = dscripition = CE = Class = HP = None
    length = len(card_text)
    if len(number_indexs) == 3:
        if number_indexs[2] - number_indexs[1] == 1:
            cost, CE, HP = int(card_text[0]), int(card_text[-2]), int(card_text[-1])
            dscripition = ''.join(str(card_text[i]) for i in range(1,length - 2))
        if number_indexs[2] - number_indexs[1] == 2:
            cost, CE, HP = int(card_text[0]), int(card_text[-3]), int(card_text[-1])
            Class = str(card_text[-2])
            dscripition = ''.join(str(card_text[i]) for i in range(1,length - 3))
    elif len(number_indexs) == 2:
        if number_indexs.count(0) == 0:
            CE, HP = int(card_text[number_indexs[0]]), int(card_text[number_indexs[1]])
            if number_indexs[1] - number_indexs[0] == 2:
                Class = str(card_text[number_indexs[0] + 1])
            dscripition = ''.join(str(card_text[i]) for i in range(0, number_indexs[0]))
        elif number_indexs[1] == length - 1:
            cost, HP = int(card_text[number_indexs[0]]), int(card_text[number_indexs[1]])
            dscripition = ''.join(str(card_text[i]) for i in range(number_indexs[0] + 1, number_indexs[1]))
        elif number_indexs[1] == length - 2:
            cost, CE = int(card_text[number_indexs[0]]), int(card_text[number_indexs[1]])
            Class = str(card_text[number_indexs[1] + 1])
            dscripition = ''.join(str(card_text[i]) for i in range(number_indexs[0] + 1, number_indexs[1]))
    elif len(number_indexs) == 1:
        if number_indexs.count(0) > 0:
            cost = int(card_text[0])
            dscripition = ''.join(str(card_text[i]) for i in range(1,length))
        elif number_indexs[0] == length - 1:
            HP = int(card_text[number_indexs[0]])
            dscripition = ''.join(str(card_text[i]) for i in range(0,length - 1))
        elif number_indexs[0] == length - 2:
            CE = int(card_text[number_indexs[0]])
            Class = str(card_text[length - 1])
            dscripition = ''.join(str(card_text[i]) for i in range(0,length - 2))
    elif len(number_indexs) == 0:
        dscripition = ''.join(str(card_text[i]) for i in range(0,length))
    return {'cost':cost,'dscripition':dscripition,'CE':CE,'Class':Class,'HP':HP},dscripition

# 第一步，获取图片
file_names = ['voyage-to-the-sunken-city',\
              'fractured-in-alterac-valley',\
              'united-in-stormwind','forged-in-the-barrens',\
              'madness-at-the-darkmoon-faire','scholomance-academy','ashes-of-outland',\
              'descent-of-dragons','saviors-of-uldum','rise-of-shadows',\
              'rastakhans-rumble','the-boomsday-project','the-witchwood',\
              'kobolds-catacombs']

for file_name in file_names:
    driver = webdriver.Chrome()  
    #"设置浏览器宽1600、高800显示"
    driver.set_window_size(1300, 800)
    #js="window.scrollTo(0,document.body.scrollHeight)" #从0的位置向下翻动到document.body.scrollheight的位置
    #driver.execute_script(js) #备选方式
    driver.implicitly_wait(12) 
    if file_name == 'voyage-to-the-sunken-city':
        #此为最初尝试版本的保留，许多操作没有实际的必要性
        driver.get("https://hs.blizzard.cn/")
        elements = driver.find_elements(By.CLASS_NAME,'enter')
        for element in elements:
            if element.find_element(By.LINK_TEXT,'进入官网'):
                element.click()
        sunkencity = driver.find_element(By.CSS_SELECTOR,'.target')
        sunkencity.click()
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if '探寻沉没之城' in driver.title:
                break
    elif file_name == 'the-witchwood':
        driver.get("https://hs.blizzard.cn/gameguide/the-witchwood/cards/")
    elif file_name == 'kobolds-catacombs':
        driver.get("https://hs.blizzard.cn/article/16/11477")
    else:
        driver.get("https://hs.blizzard.cn/gameguide/cards/?cardset={0}".format(file_name))
    time.sleep(3) #缓冲时间
    for i in range(60):
        #自动滚轮的代码
        ActionChains(driver).key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
        time.sleep(0.5)
    time.sleep(3) #缓冲时间
    pictures = driver.find_elements(By.CSS_SELECTOR,'li>img[src]')
    if file_name == 'kobolds-catacombs':
        pictures = driver.find_elements(By.CSS_SELECTOR,'.imgArr>p>img')
    i = 1
    for picture in pictures:
        print(picture.get_attribute('src'))
        r = requests.get(picture.get_attribute('src'))
        with open('D://heartstone/{0}/cards_img/00{1}.png'.format(file_name,i),'wb') as f:
            f.write(r.content)
        i += 1
    driver.quit()

sizes = [170,170,170,170,170,135,135,140,135,136,135,136,135,135]

#第二步，在线获取图片的文字信息，数据预处理（不能离线处理是因为缺乏实现图片识别的机器学习人工智能的能力）
avalible_files = ['voyage-to-the-sunken-city','forged-in-the-barrens','ashes-of-outland','rise-of-shadows',\
                  'the-witchwood','fractured-in-alterac-valley','united-in-stormwind','madness-at-the-darkmoon-faire',\
                      'scholomance-academy','descent-of-dragons','saviors-of-uldum']

dic = {}
for i in range(14):
    dic[file_names[i]] = sizes[i]
cards = []
for file_name in file_names:
    if file_name in avalible_files:
        continue
    n = 1
    if file_name == 'rastakhans-rumble':
       n = 128
    while n < dic[file_name] + 1:
        wb = webdriver.Chrome()
        wb.implicitly_wait(10)
        wb.get('https://www.gaitubao.com/tupian-wenzi')
        input_button = wb.find_element(By.CSS_SELECTOR,'#btn-upload>input')
        input_button.send_keys(r'D://heartstone/{0}/cards_img/00{1}.png'.format(file_name,n)) #要加一个'r'否则会报错,r为反转义符号
        time.sleep(19)
        copy_button = wb.find_element(By.CSS_SELECTOR,'#btn-copy')
        copy_button.click()
        card_text = pd.read_clipboard(header=None).values
        num_indexs = []
        for i in range(0,len(card_text)): 
            if re.match(r'\[\'(([0-9]{2})|([0-9]))\'\]', str(card_text[i])):
                num_indexs.append(i)  
        print(num_indexs)
        newcard,dscripition = card(num_indexs,card_text)
        dscripition = re.sub(r'\[\'', '', str(dscripition))
        dscripition = re.sub(r'\'\]', '', str(dscripition))
        newcard['dscripition'] = dscripition
        print("从剪贴板中得到的array：\n",str(newcard))
        newdf = pd.DataFrame.from_dict([newcard])
        newdf.to_csv('D://heartstone/{0}/cards.csv'.format(file_name),mode = 'a')#储存形式 —— CSV
        wb.close()
        n += 1


