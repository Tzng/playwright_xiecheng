import datetime
import html
import random
import re
from time import sleep
import pandas as pd

from playwright.sync_api import Playwright, sync_playwright, expect, ElementHandle

base_url = "https://i.meituan.com/deal/704386554/feedback"


# 转换为Playwright所需的Cookie格式
def convert_to_playwright_cookies(json_obj, domain):
    cookies = []
    for name, value in json_obj.items():
        cookie = {
            'name': name,
            'value': value,
            'domain': domain,
            'path': '/',
            'expires': -1  # Session cookie
        }
        cookies.append(cookie)
    return cookies


# 导入crawlUtil
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    # 这里写自己的cookie
    cookies = {

    }
    playwright_cookies = convert_to_playwright_cookies(cookies, 'i.meituan.com')
    context = browser.new_context()
    context.add_cookies(playwright_cookies)
    page = context.new_page()
    page.goto(base_url)
    # 获取account的值，得到总数
    total_review = page.query_selector('.account').inner_text()
    # 10条一页，计算总页数
    total_page = int(total_review) // 10 + 1
    # 定义一个数据列表
    data = []
    # 循环页数
    for i in range(total_page):
        # 取出class为dd-padding的元素数组
        reviews = page.query_selector_all('.dd-padding')
        for review in reviews:
            # 取出下面class为username的单个元素作为username
            user_name = review.query_selector('.username').inner_text()
            # 取出class为comment的元素作为评论
            content = review.query_selector('.comment').inner_text()
            # 取出class为time的元素作为时间
            review_time = review.query_selector('.time').inner_text()
            # 取出class为stars的全部img
            stars = review.query_selector_all('.stars img')
            # 循环判断是几个星星
            score = 0
            for star in stars:
                # 如果class包含：star_full，说明是满星
                if 'star_full' in star.get_attribute('class'):
                    score += 1
            # 打印信息
            print('用户名：', user_name)
            print('时间：', review_time)
            print('评分：', score)
            print('内容：', content)
            print('---------------------------------')
            # 创建包含点评信息的字典并添加到数据列表
            review_dict = {
                'user_name': user_name,
                'review_time': review_time,
                'score': score,
                'content': content
            }
            data.append(review_dict)
        # 休息2到3秒
        # sleep(random.randint(10, 20))
        # 打印下当前数据的总数
        print('当前数据总数：', len(data))
        break
        # 点击文字为下一页的a标签
        # next_page = page.query_selector('a:has-text("下一页")')
        # if next_page:
        #     # 如果a标签的class包含disabled，说明是最后一页
        #     if 'disabled' in next_page.get_attribute('class'):
        #         break
        #     next_page.click()
    # 将data写入到一个json文件中去
    with open('美团.json', 'w') as f:
        f.write(str(data))
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
