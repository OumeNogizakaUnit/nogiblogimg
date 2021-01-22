import sys
from datetime import datetime
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup

from nogiblogimg import BASE_URL, MEMBER_LIST, ua


def get_one_page(month, page, base_dir):
    # 最初に指定したページの処理の関数

    print("開始します")
    page_num = get_page_num(month)
    page_num_mux = page_num -1
    for blogpage in range(page, page_num):
        nogihtml = get_html(month, blogpage)
        print(str(month)+"の"+str(blogpage)+"/"+str(page_num_mux)+"ページ処理開始します")
        save_times = get_time(nogihtml)
        save_names = get_name(nogihtml)
        save_image_list = get_images(nogihtml)
        save_image_data(save_image_list, save_names, save_times, base_dir)
        print(str(month)+"の"+str(blogpage)+"/"+str(page_num_mux)+"ページの処理終了します")


def get_html(month, page):
    # HTMLを取得するための処理
    query = {'p': page, 'd': month}
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
    # その月が何ページあるかどこのページからでも取得する関数
    bloghtml = get_html(month, page=1)
    pagehtml = bloghtml.find('div', class_="paginate")
    pagelist_el = pagehtml.find_all('a')
    page_str_list = [el.text.strip() for el in pagelist_el]
    page_list = []
    for page in page_str_list:
        try:
            page_num = int(page)
            page_list.append(page_num)
        except ValueError:
            continue
    page_max = 1+max(page_list)
    return page_max


def get_time(nogihtml):
    # 記事の投稿日時を取得する関数
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
    # 記事の投稿者を取得する関数
    name_elements = nogihtml.find_all('span', class_="author")

    jpnames = []
    for name_element in name_elements:
        namehtml = name_element.get_text()
        namestr = str(namehtml)
        jpnames.append(namestr)
    save_names = neme_conversion(jpnames)
    return save_names


def neme_conversion(jpnames):
    # 取得した名前を英語に変換
    engnames = []
    for jpname in jpnames:
        if jpname in MEMBER_LIST:
            engnames.append(MEMBER_LIST[jpname])
        else:
            print("未登録のメンバーです、unknownとして処理します。")
            engnames.append("unknown")
    return engnames


def get_images(nogihtml):
    # 記事から画像URLを取得
    save_images = []
    emozi = re.compile(r'image-embed')
    article_bodys = nogihtml.find_all('div', class_="entrybody")
    for article_body in article_bodys:
        images = article_body.findAll('img')
        nonemozi_images = [nonemozi for nonemozi in images if not re.search(emozi,str(nonemozi))]
        image_urls = [url.get('src','') for url in nonemozi_images]
        image_urls2 = [i for i in image_urls if not i == '']
        save_images.append(image_urls2)
    return save_images


def save_image_data(save_image_list, save_names, save_times, base_dir):
    # 保存の準備の関数
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
