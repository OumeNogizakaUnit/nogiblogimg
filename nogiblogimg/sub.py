import click
import os
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

from nogiblogimg.member_list import member_list


def get_one_page(month, page, savedir):
    #指定したページの処理の関数
    page_URL="http://blog.nogizaka46.com/?p="+str(page)+"&d="+str(month)
    print(page_URL)
    nogihtml = get_html(page_URL)
    save_times = get_time(nogihtml)
    print(save_times)
    save_names = get_name(nogihtml)
    print(save_names)
    save_image_list = get_images(nogihtml)
    image_data(save_image_list, save_names, save_times)


def get_html(page_URL):
    ua ="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"\
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100"
    response = requests.get(page_URL, headers={"User-Agent": ua})
    nogizakahtml = BeautifulSoup(response.content, "html.parser")
    bloghtml = nogizakahtml.find('div', class_="right2in")
    return bloghtml 


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
    memberlist = member_list()
    engnames = []
    for jpname in jpnames:
        if jpname in memberlist:
            engnames.append(memberlist[jpname])
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
        save_images.append(images)
    return save_images
def image_data(save_image_list, save_names, save_times):
    #保存の準備の関数
    for num, image_urls in enumerate(save_image_list):
        print(str(num))
        name = save_names[num]
        time = save_times[num]
        for index, image_url in enumerate(image_urls):
            save_url = image_url['src']
            save_image = requests.get(save_url)
            saveder = "./img/"+name+"/"
            save_name = name+"_"+time+"_"+str(index)+".jpg"
            save_der_name = saveder+save_name
            print(save_der_name)
            if os.path.isdir(saveder):
                print("ディレクトリが存在します")
                save(save_der_name, save_image)
            else:
                 print("ディレクトリが存在しません作成し続行します")
                 os.makedirs(saveder)
                 save(save_der_name, save_image)
def save(save_der_name, save_image):
    #保存の関数 
    with open(save_der_name,'wb') as file:
        file.write(save_image.content)
