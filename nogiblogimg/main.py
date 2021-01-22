import click

from nogiblogimg.sub import get_one_page


@click.command()
def main():
    #201111~最新まで
    month = "201111"
    #取得開始したいページ
    page = 1
    base_dir = './img'
    get_one_page(month, page, base_dir)
