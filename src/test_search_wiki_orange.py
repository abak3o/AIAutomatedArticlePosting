import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.wikipedia.org/")
        page.get_by_role("searchbox", name="Search Wikipedia").click()
        page.get_by_role("searchbox", name="Search Wikipedia").fill("orange")
        page.get_by_role("searchbox", name="Search Wikipedia").press("Enter")
        page.get_by_role("button", name="Search").click()
        page.goto("https://ja.wikipedia.org/wiki/%E3%82%AA%E3%83%AC%E3%83%B3%E3%82%B8_(%E6%9B%96%E6%98%A7%E3%81%95%E5%9B%9E%E9%81%BF)")

        # ---------------------
        context.close()
        browser.close()


with sync_playwright() as playwright:
    run(playwright)
