### Project: 深交所定期公告PDF下载多进程
### process: 进入深交所官网定期公告下载页面下载报告PDF
### Author: WENHUI YANG
### Date: 2023-03-17
import time
from multiprocessing import Pool
from typing import Set, Any

import requests
import urllib.request
import urllib.parse
import json
import os
import re

URL = 'http://www.szse.cn/api/disc/announcement/annList?random=0.09127020156653809'
URL1 = 'http://www.szse.cn/api/disc/info/download?id='

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'HOST': 'www.szse.cn',
    'Origin': 'http://www.szse.cn',
    'Referer': 'http://www.szse.cn/disclosure/listed/notice/index.html',
    'X-Request-Type': 'ajax',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/111.0.0.0 Safari/537.36',
}

pdf_list = []  # 保存pdf链接地址
title_list = []  # 保存pdf文件名
publishTime_list = []  # 保存时间
secCode_list = []  # 股票代码
code_name_list = []  # 股票代码＋公司名


def get_pdf_info(page_num):
    """
    请求表格内容
    Parameter:
        page_num: int  页码
        page_size: int 页数（固定：30）
    Return:
        res: list 获取的表格内容
    """
    for page in range(1, page_num + 1):
        body = {
            "channelCode": [
                "fixed_disc"
            ],
            "pageSize": 50,
            "pageNum": page,
            "stock": []
        }

        rp = requests.post(URL, headers=headers, data=json.dumps(body))
        rp_dict = rp.json()
        info_all = rp_dict['data']
        for info in info_all:
            pdf_list.append(info['id'])
            title_list.append(info['title'])
            publishTime_list.append(info['publishTime'][:10])
            code_name_l = info['secCode'][0] + ' ' + info['secName'][0]
            code_name_list.append(code_name_l)


def validateTitle(title):
    """
    去除文件名中的特殊符号
    Parameter:
        title: str  需要处理的文件名称
    Return:
        new_title: str 没有特殊符号的文件名
    """
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


def download_and_extract(saveDir, pdf, title, publishTime, codeName, n):
    """
    根据给定的URL地址下载文件
    Parameter:

    """
    saveDir_subdirectory = saveDir + '/' + codeName
    try:
        save_path = os.path.join(saveDir_subdirectory, title + str(publishTime) + '.pdf')
        urllib.request.urlretrieve(URL1 + pdf, save_path)
        print(f'NO.{n} Downloading {title}')
    except ConnectionError:
        print(f'{title} 下载失败')


## 下载
if __name__ == "__main__":
    pageNumber_input = input("Please enter a page number: ")
    saveDir_input = input("Please enter a directory: ")
    pageNumber = int(pageNumber_input)
    saveDir_root = str(saveDir_input)

    # 获取所有需求信息
    get_pdf_info(pageNumber)

    # 新建每个上市公司文件夹
    code_name_list2 = list(set(code_name_list))
    for code_name in code_name_list2:
        os.mkdir(saveDir_root + '/' + code_name)  # mac的路径

    # 开始下载
    start_time = time.time()
    pool = Pool(processes=5)
    print(f'-----共有{len(pdf_list)}份报告-----')

    for pdf1, title1, publishTime1, codeName1, no \
            in zip(pdf_list, title_list, publishTime_list, code_name_list, range(1, len(pdf_list) + 2)):

        pool.apply_async(download_and_extract, args=(saveDir_root, pdf1, title1, publishTime1, codeName1, no,))

    pool.close()
    pool.join()
    cost = time.time() - start_time

    print(f"下载完毕(*^▽^*)\n共用时：{cost:.2f}s")
