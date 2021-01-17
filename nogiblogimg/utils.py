

def fetch_one_month(month, savedir):
    print("fetch_one_monthやで")
    text = "月のHTMLを取得"
    pagenate = find_pagenate(text)
    for i in pagenate:
        fetch_one_page(month, i, savedir)


def find_pagenate(text):

    return [0, 1, 2, 3]


def fetch_one_page(month, page, savedir):
    print("fetch_one_pageやで")
    text = f"{page}ページのHTMLを取得"
    print(text)
    article_list = find_article_list(text)
    for article in article_list:
        fetch_one_article(article, savedir)


def fetch_one_article(article, savedir):
    name = find_name(article)
    time = find_time(article)
    imageurls = find_imageurls(article)
    decomailerurls = find_decomailer(article)
    for imageurl in imageurls:
        save_image(imageurl, savedir)

    for decomailerurl in decomailerurls:
        save_decomailer(decomailerurl, savedir)

def find_article_list(text):
    return ["article1", "article2", "article3"]


def find_name(text):
    return "中村麗乃"


def find_time(text):
    return "202012120930"


def find_imageurls(text):
    # デコメーラーのサムネ画像も含む
    return ["<img></img>", "<a href=decomailer></a>"]


def find_decomailer(text):
    # デコメーラーのURLを取得する関数
    return ["<a href=decomailer></a>"]

def save_image(imageurl, savedir):
    # imageurlの画像を保存
    return None


def save_decomailer(decomailerurl, savedir):
    # デコメーラーの画像を保存
    return None
