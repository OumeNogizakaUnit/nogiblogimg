import click
import re
from nogiblogimg.sub import get_one_page

@click.command()
def main():
    month = "202001"
    page = 19
    base_dir = './img'
    get_one_page(month, page, base_dir)


