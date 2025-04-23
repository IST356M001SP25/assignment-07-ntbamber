import re
from playwright.sync_api import Playwright, sync_playwright
from menuitemextractor import extract_menu_item
from menuitem import MenuItem
import pandas as pd

def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    #print("navigating to Tully's menu page...") #Debugging
    page.goto("https://www.tullysgoodtimes.com/menus/", timeout=60000)

    menu_data = []
    sections = page.query_selector_all("h3.foodmenu__menu-section-title")
    #print(f"found {len(sections)} menu sections") #Debugging

    for section in sections:
        category = section.inner_text().strip()
        #print(f"\n section: {category}") #Debugging

        # Get the container div with menu items
        container = section.evaluate_handle("el => el.nextElementSibling?.nextElementSibling")

        items = container.query_selector_all("div.foodmenu__menu-item")
        #print(f"found {len(items)} menu items") #Debugging

        for item in items:
            raw_text = item.inner_text().strip()
            menu_item = extract_menu_item(category, raw_text)
            #print(f"confirm: {menu_item.name}") #Debugging
            menu_data.append(menu_item.to_dict())

    # Save to CSV
    df = pd.DataFrame(menu_data)
    df.to_csv("cache/tullys_menu.csv", index=False)
    #print(f"\n Saved {len(menu_data)} items to cache/tullys_menu.csv") #Debugging
    #print(f"DataFrame shape: {df.shape}") #Debugging

    context.close()
    browser.close()


with sync_playwright() as playwright:
    tullyscraper(playwright)
