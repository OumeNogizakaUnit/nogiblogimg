import click

from nogiblogimg.utils import get_one_page


@click.command()
def main():
    # 取得開始したい月 "201111"以上
    start_month = "202006"
    # 取得終了したい月 最新の月以下
    end_month = "202012"
    # 取得開始したいページ(基本1でおけ)
    page = 1
    base_dir = './img'
    get_one_page(page, base_dir, start_month, end_month)
