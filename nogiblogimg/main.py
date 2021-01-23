import click

from nogiblogimg.datemonth import bigmonth2str, datetime2bigmonth
from nogiblogimg.utils import get_one_month


@click.command()
@click.option('-s',
              '--start',
              help='集計開始月',
              default='201111',
              show_default=True,
              type=click.DateTime(formats=['%Y%m']))
@click.option('-e',
              '--end',
              help='集計終了月',
              default='201112',
              show_default=True,
              type=click.DateTime(formats=['%Y%m']))
@click.argument('savedir',
                type=click.Path())
def main(start, end, savedir):
    '''
    SAVEDIR に画像を保存する
    '''
    print("開始")
    bigstart_month = datetime2bigmonth(start)
    bigend_month = datetime2bigmonth(end)
    for big_month in range(bigstart_month, bigend_month+1):
        month = bigmonth2str(big_month)
        get_one_month(savedir, month)
    print("終了")
