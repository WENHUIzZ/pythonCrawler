"""
@project: 多进程爬取豆瓣电影评分top250
@point: xpath的运用， 多进程池的运用
@to do: 如何去掉text()的引号，因为出来的是一个list所以值带有引号
"""
import requests
from multiprocessing import Pool
from lxml import etree
import time


HEADER = {"User-Agent":
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/95.0.4638.54 Safari/537.36"}


def concat_title(t_l):
    final_title = ""
    for t in t_l:
        t = "".join(t.split())
        final_title += t
    return final_title


def get_info(url):
    rp = requests.get(url, headers=HEADER, timeout=30)

    if rp.status_code == 200:
        html = etree.HTML(rp.text)
        div_rank_all = html.xpath("//div[@class='pic']")
        div_info_all = html.xpath("//div[@class='info']")
        for div1, div2 in zip(div_rank_all, div_info_all):
            # rank
            rank = div1.xpath("./em/text()")

            # title
            title_list = div2.xpath("./div[@class='hd']/a//span/text()")
            title = concat_title(title_list)
            # details
            details = div2.xpath("./div[@class='bd']/p/text()")
            details = concat_title(details)
            # score
            score = div2.xpath("./div[@class='bd']/div[@class='star']/span[@class='rating_num']/text()")
            # grader
            grader = div2.xpath("./div[@class='bd']/div[@class='star']/span[4]/text()")
            # summary
            summary = div2.xpath("./div[@class='bd']/p[@class='quote']/span/text()")

            print("序号：", rank)
            print("电影名称：", title)
            print("介绍：", details)
            print("得分：", score)
            print("评分人：", grader)
            print("简介：", summary)
            print("------------------")


def get_all_info():
    start_time = time.time()
    pool = Pool(processes=5)
    movie_url_list = [f"https://movie.douban.com/top250?start={i}&filter=" for i in range(0, 251, 25)]
    for u in movie_url_list:
        pool.apply_async(get_info, args=(u,))   # 非阻塞0.53， 阻塞2.21
    pool.close()
    pool.join()
    # pool.map(get_info, movie_url_list)   乱序的
    print(time.time() - start_time)


if __name__ == "__main__":
    get_all_info()
