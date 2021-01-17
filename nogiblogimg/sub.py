import click
import requests
from bs4 import BeautifulSoup
import re
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


def get_html(page_URL):
    ua ="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"\
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100"
    response = requests.get(page_URL, headers={"User-Agent": ua})
    nogizakahtml = BeautifulSoup(response.content, "html.parser")
    bloghtml = nogizakahtml.find('div', class_="right2in")
    return bloghtml 


def get_time(bloghtml):
    #記事の投稿日時を取得する関数
    time_elements = bloghtml.find_all('div', class_='entrybottom')
    savetimes = []
    for time_element in time_elements:
        timehtml = time_element.get_text()
        timestr = str(timehtml)
        time_data = timestr[1:17]
        time = time_data.replace(' ', '[')
        savetimes.append(time)
    return savetimes
    

def get_name(bloghtml):
    #記事の投稿者を取得する関数
    name_elements = bloghtml.find_all('span', class_="author")
    
    JPnames = []
    for name_element in name_elements:
        namehtml = name_element.get_text()
        namestr = str(namehtml)
        JPnames.append(namestr)
    save_names = neme_conversion(JPnames)    
    return save_names
def neme_conversion(JPnames):
    #取得した名前を英語に変換
    memberlist = member_list()
    ENGnames = []
    for JPname in JPnames:
        ENGnames.append(memberlist[JPname])
    return ENGnames
def get_images():
    #記事から画像URLを取得
    print("a")  

def save():
    #保存する関数
    print("a")  

