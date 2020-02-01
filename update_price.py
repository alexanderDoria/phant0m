import requests
from lxml import html
import sys

# check arguments for ticker
if len(sys.argv) == 2:
    ticker = sys.argv[1].upper()
else:
    ticker = "QQQ"


def get_tree(url):
    page = requests.get(url)
    return html.fromstring(page.content)


def process_row(cells):
    last = {}
    last['date'] = cells[0]
    last['open'] = cells[1]
    last['high'] = cells[2]
    last['low'] = cells[3]
    last['close'] = cells[4]
    last['adj_close'] = cells[5]
    last['volume'] = cells[6]
    return last


def get_recent_data(ticker):
    url = "https://finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker
    try:
        tree = get_tree(url)
    except:
        print("error reaching URL: ", url)
        exit()

    cells = tree.xpath(
        '//*[@data-test="historical-prices"]//tbody//tr[1]//td//text()')

    last = process_row(cells)
    return last


print(get_recent_data(ticker))
