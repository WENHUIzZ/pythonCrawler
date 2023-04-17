import urllib.request
import urllib.parse
import json
import sys
import os
import re
import requests

url = 'http://www.szse.cn/api/disc/announcement/annList?random=0.09127020156653809'

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

body = {
    "channelCode": [
        "fixed_disc"
    ],
    "pageSize": 50,
    "pageNum": 2,
    "stock": []
}

rp = requests.post(url, headers=headers, data=json.dumps(body))
rp_dict = rp.json()
print(rp_dict['data'][0]['id'])

# bigCategoryId = [""]
# bigIndustryCode = [""]
# channelCode = [""]
# plateCode = [""]
# seDate = ["", ""]
#
#
# def get_pdf(pageNum, pageSize):
#     """请求表格内容
#           Parameter:
#               pageNum: str  页码
#               pageSize: int 页数（固定：30）
#           Return:
#               res: list 获取的表格内容
#     """
#     params = {
#         'seDate': seDate,
#         'bigCategoryId': bigCategoryId,
#         'bigIndustryCode': bigIndustryCode,
#         'channelCode': channelCode,
#         'pageNum': pageNum,
#         'pageSize': pageSize,
#         'plateCode': plateCode
#     }
#
#     request = urllib.request.Request(url=url, headers=headers)
#     form_data = json.dumps(params).encode()  # urllib.parse.urlencode(params).encode()
#     response = urllib.request.urlopen(request, form_data)
#     res_list = response.read().decode()
#     res = json.loads(res_list)
#     print(res)
#
