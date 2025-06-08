from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse

def scrape_with_browser(url):
    links = set()
    text = ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"[Загрузка] {url}")
        try:
            page.goto(url, timeout=60000)
            page.wait_for_selector("a", timeout=10000)  # Ждём появления ссылок

            text = page.inner_text("body")

            anchors = page.query_selector_all("a")
            print(f"[Playwright] Найдено якорей: {len(anchors)}")
            for a in anchors:
                href = a.get_attribute("href")
                if href:
                    full_url = urljoin(url, href)
                    if urlparse(full_url).netloc == urlparse(url).netloc:
                        links.add(full_url)

        except Exception as e:
            print(f"[Ошибка Playwright] {e}")
        finally:
            browser.close()

    return text, list(links)
