import os
from playwright.sync_api import Playwright, sync_playwright, expect


user_dir = '/tmp/playwright'


if not os.path.exists(user_dir):
    os.makedirs(user_dir)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch_persistent_context(
            user_dir,
            headless=False,
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
        )
        
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://m.dafabet.com/pt")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)