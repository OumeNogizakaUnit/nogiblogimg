import click
import os
import sys
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from pathlib import Path

from nogiblogimg import MEMBER_LIST, BASE_URL


def get_one_page(month, page, base_dir):
    #最初に指定したページの処理の関数

    print("開始します")
    nogihtml = get_html(month, page)
    print(str(month)+"の"+str(page)+"ページ処理開始します")
    save_times = get_time(nogihtml)
    save_names = get_name(nogihtml)
    save_image_list = get_images(nogihtml)
    save_image_data(save_image_list, save_names, save_times, base_dir)
    print(str(month)+"の"+str(page)+"ページの処理終了します")

def get_html(month, page):
    #HTMLを取得するための処理
    ua ="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"\
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100"
    query = {'p': page,'d': month}
    response = requests.get(BASE_URL, params=query, headers={"User-Agent": ua})
    if response.status_code != 200:
        print("サイトに入るのを拒否られました,終了します")
        print(response.text)
        sys.exit()
    else:
        nogizakahtml = BeautifulSoup(response.content, "html.parser")
        bloghtml = nogizakahtml.find('div', class_="right2in")
    return bloghtml


def get_page_num(month):
    #その月が何ページあるかどこのページからでも取得する関数
    bloghtml = get_html(month, page=1)
    pagehtml = bloghtml.find('div', class_="paginate")
    pagelist_el = pagehtml.find_all('a')
    page_str_list = [el.text.strip() for el in pagelist_el]
    page_list = []
    for page in page_str_list:
        try:
            page_num = int(page)
            page_list.append(page_num)
        except ValueError as error:
            continue
    page_max = max(page_list)
    return page_max


def get_time(nogihtml):
    #記事の投稿日時を取得する関数
    time_elements = nogihtml.find_all('div', class_='entrybottom')
    savetimes = []
    for time_element in time_elements:
        timehtml = time_element.get_text()
        timestr = timehtml.strip().split("｜")[0]
        # timestr sample: 2020/01/31 23:50
        timedata = datetime.strptime(timestr, '%Y/%m/%d %H:%M')
        # article_timestr sample: 202001312350
        article_timestr = timedata.strftime('%Y%m%d%H%M')
        savetimes.append(article_timestr)
    return savetimes
    

def get_name(nogihtml):
    #記事の投稿者を取得する関数
    name_elements = nogihtml.find_all('span', class_="author")
    
    jpnames = []
    for name_element in name_elements:
        namehtml = name_element.get_text()
        namestr = str(namehtml)
        jpnames.append(namestr)
    save_names = neme_conversion(jpnames)    
    return save_names


def neme_conversion(jpnames):
    #取得した名前を英語に変換
    engnames = []
    for jpname in jpnames:
        if jpname in MEMBER_LIST:
            engnames.append(MEMBER_LIST[jpname])
        else:
            print("未登録のメンバーです、unknownとして処理します。")
            engnames.append("unknown")
    return engnames


def get_images(nogihtml):
    #記事から画像URLを取得
    save_images = []
    article_bodys = nogihtml.find_all('div', class_="entrybody")  
    for  article_body in article_bodys:
        images = article_body.findAll('img')
        image_urls = [url.get('src', '') for url in images]
        save_images.append(image_urls)
    return save_images


def save_image_data(save_image_list, save_names, save_times, base_dir):
    #保存の準備の関数
    save_base_path = Path(base_dir)
    for imagedata in zip(save_image_list, save_names, save_times):
        imageurls = imagedata[0]
        name = imagedata[1]
        time = imagedata[2]
        save_path = Path(save_base_path, name)
        if save_path.exists() is False:
            save_path.mkdir(parents=True)
        save_image_data_one(imageurls, name, time, save_path)


def save_image_data_one(imageurls, name, time, save_path):
    for index, imageurl in enumerate(imageurls):
        res = requests.get(imageurl)
        image_suffix = imageurl.split('.')[-1]
        image_filename = f'{name}_{time}_{index:0>3}.{image_suffix}'
        image_path = Path(save_path, image_filename)
        with image_path.open('wb') as fd:
            fd.write(res.content)
        print(image_path)
