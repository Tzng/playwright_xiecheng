import uuid
import re
import json
import random
import re
from time import sleep

import pymysql

from playwright.sync_api import Playwright, sync_playwright, expect, ElementHandle

base_url = "https://passport.meituan.com/useraccount/ilogin"

# 导入crawlUtil
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    # browser 设置为手机模式

    context = browser.new_context(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1")
    page = context.new_page()
    page.goto(base_url)
    # 等待1分钟
    sleep(60)
    context.storage_state(path='meituan_login.json')
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
