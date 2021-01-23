import click

from nogiblogimg.datemonth import bigmonth2str, str2bigmonth
from nogiblogimg.utils import get_one_month


@click.command()
def main():
    # 取得開始したい月 "201111"以上
    start_month = "201111"
    # 取得終了したい月 最新の月以下
    end_month = "201202"
    # セーブ場所
    base_dir = './img'
    print("開始")
    bigstart_month = str2bigmonth(start_month)
    bigend_month = str2bigmonth(end_month)
    for big_month in range(bigstart_month, bigend_month+1):
        month = bigmonth2str(big_month)
        get_one_month(base_dir, month)
    print("終了")
