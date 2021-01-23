from datetime import datetime


def str2bigmonth(datestr):
    '''
    datestr を bigmonth に変換する関数
    例
    202012 -> 2020*12 + 12 = 240252
    '''
    date = datetime.strptime(datestr, '%Y%m')
    year = date.year
    month = date.month
    return year * 12 + month


def bigmonth2str(bigmonth):
    '''
    bigmonth を 文字列に変換する関数
    例
    240252 -> 202012
    '''
    year = int(bigmonth / 12)
    month = bigmonth % 12
    if month == 0:
        year -= 1
        month = 12
    return f'{year}{month:0>2}'
