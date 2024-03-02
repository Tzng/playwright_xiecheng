import datetime
import html
import random
import re
from time import sleep
import pandas as pd

from playwright.sync_api import Playwright, sync_playwright, expect, ElementHandle

base_url = "https://you.ctrip.com/sight/beijing1/5306.html#ctm_ref=www_hp_bs_lst"

# 导入crawlUtil
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(base_url)

    # 获取总点评数量
    total_review = page.query_selector('.moduleTitle').inner_text()
    # 打印信息
    print('总点评数量：', total_review)
    # 获取class为ant-pagination-item的元素数组，其中最后一个为最后一页的按钮
    last_page = page.query_selector_all('.ant-pagination-item')[-1]
    # 获取最后一页的页码
    last_page_num = last_page.inner_text()
    # 打印信息
    print('最后一页的页码：', last_page_num)
    # 获取下一页的按钮
    next_page = page.query_selector('.ant-pagination-next > .ant-pagination-item-comment > a')
    # 定义一个数据列表
    data = []
    # 循环页数
    for i in range(int(last_page_num)):
        # 获取当前页的所有点评
        reviews = page.query_selector_all('div.commentList > div')
        # 循环点评
        for review in reviews:
            # 获取点评的用户名
            user_name = review.query_selector('.userName').inner_text()
            # 获取点评的时间
            review_time = review.query_selector('.commentTime').inner_text()
            # 获取IP属地
            ip_location = review.query_selector('.ipContent').inner_text()
            # review_time需要删除IP属地部分
            review_time = review_time.replace(ip_location, '')
            # 获取点评的评分
            scoreText = review.query_selector('.averageScore').inner_text()
            # 使用正则获取数字
            score = re.findall(r'\d+', scoreText)[0]
            # 获取点评的内容
            content = review.query_selector('.commentDetail').inner_text()
            # 打印信息
            print('用户名：', user_name)
            print('时间：', review_time)
            print('评分：', scoreText)
            print('评分数：', score)
            print('内容：', content)
            print('IP属地：', ip_location)
            print('---------------------------------')
        # 创建包含点评信息的字典并添加到数据列表
        review_dict = {
            'user_name': user_name,
            'review_time': review_time,
            'score': score,
            'content': content,
            'ip_location': ip_location
        }
        data.append(review_dict)
        # 如果有下一页
        if next_page:
            # 休息1 ~ 3秒
            sleep(random.randint(1, 3))
            # 点击下一页
            next_page.click()
        else:
            # 否则退出循环
            break
    # 将对象列表转换为DataFrame
    df = pd.DataFrame(data)
    df.to_excel('output.xlsx', index=False)
    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
