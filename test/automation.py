
from playwright.sync_api import sync_playwright

def search_google(query):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.google.com")
        page.fill("input[name='q']", query)
        page.press("input[name='q']", "Enter")
        page.wait_for_timeout(3000)
        results = page.text_content("body")
        browser.close()
        return results[:1000]
