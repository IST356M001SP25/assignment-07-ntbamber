import re
from playwright.sync_api import Playwright, sync_playwright
from menuitemextractor import extract_menu_item
from menuitem import MenuItem
import pandas as pd

def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    #page.goto("https://www.tullysgoodtimes.com/menus/")
    page.goto("https://web.archive.org/web/20241111165815/https://www.tullysgoodtimes.com/menus/")

    titles = page.query_selector_all("h2.menu-section-title")

    all_items = []

    for title_element in titles:
        title_text = title_element.inner_text().strip()

        # Navigate to the next `.row` element
        row_element = title_element.evaluate_handle("el => el.parentElement.nextElementSibling.nextElementSibling")
        if not row_element:
            continue

        items = row_element.query_selector_all("div.menu-item-text")

        for item in items:
            try:
                scraped_text = item.inner_text()
                menu_item = extract_menu_item(title_text, scraped_text)
                all_items.append(menu_item.to_dict())
            except Exception as e:
                print(f"Error processing item: {e}")

    df = pd.DataFrame(all_items)
    df.to_csv("cache/tullys_menu.csv", index=False)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    tullyscraper(playwright)
