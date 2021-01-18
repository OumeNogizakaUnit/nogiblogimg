import click
import requests
from bs4 import BeautifulSoup
import re
from nogiblogimg.sub import get_one_page

@click.command()
def main():
    month = "202001"
    page = 1
    get_one_page(month, page)


