"""
get photos from zhancool
"""

import requests
from lxml import etree
from requests_html import HTMLSession


def get_pic(url):

    session = HTMLSession()
    r = session.get(url)
    html = etree.HTML(r.text)
    pic_list = html.xpath('//div[@class="light-slide-content"]/img/@data-src')
    return pic_list


def download_pic(pictures_list, out_dir):
    print(f"共有{len(pictures_list)}张，请耐心等待😊")
    n = 0
    for pic_url in pictures_list:

        n += 1

        print(f"开始下载第{n}张")
        pic = requests.get(pic_url)
        with open(f"{out_dir}/{n}.jpg", "wb") as p:
            p.write(pic.content)


def main(url, out_dir):
    p_list = get_pic(url)
    download_pic(p_list, out_dir)


if __name__ == "__main__":
    URL = "https://www.zcool.com.cn/work/ZNTU4ODIwOTY=.html"
    OUT_DIR = "/Users/Zhe/站酷/贰婶呀"
    main(URL, OUT_DIR)
