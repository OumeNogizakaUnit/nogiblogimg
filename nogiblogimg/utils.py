from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from nogiblogimg import BASE_URL, MEMBER_LIST


def get_one_month(base_dir, month):
    page_num = get_page_num(month)
    for page in range(1, page_num+1):
        print(f'{month}の{page}/{page_num}ページ処理開始します')
        get_one_page(page, base_dir, month)
        # print(f'{month}の/{page_num}ページ処理終了します')


def get_one_page(page, base_dir, month):
    # 指定したページの処理の関数
    nogihtml = get_html(month, page)
    save_times = get_time(nogihtml)
    save_names = get_name(nogihtml)
    save_image_list = get_images(nogihtml)
    save_image_data(save_image_list, save_names, save_times, base_dir)


def urlget(url, query={}):
    # 共通でレスポンス投げたあとする関数
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"\
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100"
    headers = {'User-Agent': user_agent}
    res = requests.get(url,
                       params=query,
                       headers=headers)
    if res.status_code != 200:
        print(res.text)
        return None
    return res


def month_list(start_month, end_month):
    # 月のURLを取得する関数
    res = urlget(BASE_URL)
    meinnogizakahtml = BeautifulSoup(res.text, "html.parser")
    meinbloghtml = meinnogizakahtml.find('div', id="sidearchives")
    html_month_list = meinbloghtml.find_all('option')
    all_month_list = [url.get('value') for url in html_month_list]
    month_list = month_list_pro(all_month_list, start_month, end_month)
    return month_list


def month_list_pro(all_month_list, start_month, end_month):
    # 処理したい月のリストをつくる関数
    start_index = all_month_list.index(
        'http://blog.nogizaka46.com/?d='+end_month)
    end_index = all_month_list.index(
        'http://blog.nogizaka46.com/?d='+start_month)+1
    month_list = all_month_list[start_index:end_index]
    return month_list


def get_html(month, blogpage):
    # HTMLを取得するための処理
    query = {'p': blogpage, 'd': month}
    res = urlget(BASE_URL, query=query)
    nogizakahtml = BeautifulSoup(res.text, "html.parser")
    bloghtml = nogizakahtml.find('div', class_="right2in")
    return bloghtml


def get_page_num(month):
    # その月が何ページあるかどこのページからでも取得する関数
    meinnogizakahtml = get_html(month, blogpage=1)
    pagehtml = meinnogizakahtml.find('div', class_="paginate")
    pagelist_el = pagehtml.find_all('a')
    page_str_list = [el.text.strip() for el in pagelist_el]
    page_list = []
    for page in page_str_list:
        try:
            page_num = int(page)
            page_list.append(page_num)
        except ValueError:
            continue
    page_max = max(page_list)

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
    article_bodys = nogihtml.find_all('div', class_="entrybody")
    for article_body in article_bodys:
        image_els = article_body.findAll('img')
        image_urls = find_image_urls(image_els)
        save_images.append(image_urls)
    return save_images


def find_image_urls(image_els):
    allow_suffix_list = ['jpg', 'jpeg', 'png', 'svg']
    image_urls = []
    for image_el in image_els:
        image_url = image_el.get('src', '')
        if not image_url.startswith('http'):
            continue
        image_suffix = image_url.split('.')[-1]
        if image_suffix not in allow_suffix_list:
            continue
        image_urls.append(image_url)
    return image_urls


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
        res = urlget(imageurl)
        image_suffix = imageurl.split('.')[-1]
        image_filename = f'{name}_{time}_{index:0>3}.{image_suffix}'
        image_path = Path(save_path, image_filename)
        with image_path.open('wb') as fd:
            fd.write(res.content)
        print(image_path)
