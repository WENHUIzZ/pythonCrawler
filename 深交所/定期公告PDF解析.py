import pdfplumber
import camelot
import pandas as pd

# pdfplumber
with pdfplumber.open("/Users/Hui/Desktop/test/300582 英飞特/英飞特：2022年第三季度报告（更新后）2023-03-02.pdf") as pdf:
    page01 = pdf.pages[1]  # 指定页码
    # table1 = page01.extract_table()  # 提取单个表格
    table2 = page01.extract_tables()  # 提取多个表格

for row in table2:
    print(row)

