from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import datetime as dt
import re
import pandas as pd



def open_browser(url,page_count):
    if url is not None:
        with sync_playwright() as playwright:
            chromium = playwright.firefox  # or "firefox" or "webkit".
            browser = chromium.launch(headless=False)
            context = browser.new_context(
                ignore_https_errors=True, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36")
            page = context.new_page()
            page.set_default_navigation_timeout(1000000000)
            df_list = []
            for i in range(1,page_count+1):
                print("Goto Url: ",url + f"{i}")
                page.goto(url + f"{i}")
                page.wait_for_load_state()
                page.wait_for_timeout(5000)
                #page_content = page.content()
                #soup = BeautifulSoup(page_content, 'html.parser')
                company_count = len(page.query_selector_all("div.filter-list div.filter-list__item"))
                #print("company_count",company_count)

                for i in range(1,company_count+1):
                    company_name    = get_inner_text(page, f"#katilimcilar-listesi > div > div:nth-child(4) > div > div:nth-child({i}) > div.filter-list__right-wrapper > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1)")
                    company_address = get_inner_text(page, f"#katilimcilar-listesi > div > div:nth-child(4) > div > div:nth-child({i}) > div.filter-list__right-wrapper > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(2)")
                    company_contact = get_inner_text(page, f"#katilimcilar-listesi > div > div:nth-child(4) > div > div:nth-child({i}) > div.filter-list__right-wrapper > table > tbody > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1) > a")
                    company_webSite = get_inner_text(page, f"#katilimcilar-listesi > div > div:nth-child(4) > div > div:nth-child({i}) > div.filter-list__right-wrapper > table > tbody > tr:nth-child(1) > td:nth-child(2) > div:nth-child(2) > a")
                    company_Product = get_inner_text(page, f"#katilimcilar-listesi > div > div:nth-child(4) > div > div:nth-child({i}) > div.filter-list__right-wrapper > table > tbody > tr.table-detail-wrapper > td > ul")
                    expo_location   = get_inner_text(page, f"#katilimcilar-listesi > div > div:nth-child(4) > div > div:nth-child({i}) > div.filter-list__right-wrapper > table > tbody > tr:nth-child(1) > td:nth-child(3) > div.salon.table-block-content > div > div.location-name > span")
                    expo_hall       = get_inner_text(page, f"#katilimcilar-listesi > div > div:nth-child(4) > div > div:nth-child({i}) > div.filter-list__right-wrapper > table > tbody > tr:nth-child(1) > td:nth-child(3) > div.salon.table-block-content > span")
                    expo_stand      = get_inner_text(page, f"#katilimcilar-listesi > div > div:nth-child(4) > div > div:nth-child({i}) > div.filter-list__right-wrapper > table > tbody > tr:nth-child(1) > td:nth-child(3) > div.stand.table-block-content")
                    #print("company_name",company_name, company_address, company_contact, company_webSite,company_Product)

                    df_list.append(pd.DataFrame({
                        'Company Name': [company_name],
                        'Company Address': [company_address],
                        'Company Contact': [company_contact],
                        'Company Website': [company_webSite],
                        'Company Product': [company_Product.strip()],
                        'Expo Location': [expo_location],
                        'Expo Hall': [expo_hall],
                        'Expo Stand': [expo_stand]
                    }))

            df = pd.concat(df_list, ignore_index=True)

            df.to_excel('output.xlsx', index=False)

def get_inner_text(page, selector):
    try:
        result = page.evaluate(f"document.querySelector('{selector}').innerText;")
        result = re.sub(r'[\n\t]', '', result)
    except Exception as e:
        result = ""
    return result



if __name__ == "__main__":
    url = "https://istanbulmobilyafuari.com/katilimci-listesi?page="
    page_count = 74
    open_browser(url,page_count)