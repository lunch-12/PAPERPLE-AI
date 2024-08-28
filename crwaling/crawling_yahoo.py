from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util.datetime_util import convert_Yahoo_date_to_datetime
from ai_crud import upsert_newspapers
from ai_model import SQLMODEL
from util.hash_utils import get_sha256_hash


def setup_browser():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-ssl-errors=yes")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--incognito")

    # Add Image Loading inactive Flag to reduce loading time
    chrome_options.add_argument("--disable-images")
    chrome_options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images": 2}
    )
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def scroll_page(browser, pause_time=0.2, scroll_count=50):
    for _ in range(scroll_count):
        browser.find_element(by=By.TAG_NAME, value="body").send_keys(Keys.PAGE_DOWN)
        time.sleep(pause_time)


def scrape_articles(browser) -> list[SQLMODEL.NewsPaper]:
    articles = browser.find_elements(
        by=By.XPATH, value="//ul/li[contains(@class, 'js-stream-content')]"
    )
    data = []
    original_window = browser.current_window_handle  # 현재 창 핸들 저장

    for article in articles:
        try:
            _ = article.find_element(
                by=By.CSS_SELECTOR, value="[data-test-locator='catlabel']"
            ).text  # category, 카테고리 현재 값 사용하고 있지 않음, 테이블 수정 후 추가

            title = article.find_element(by=By.TAG_NAME, value="h3").text
            image_tag = article.find_element(by=By.TAG_NAME, value="img")
            image = image_tag.get_attribute("src")

            link = article.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
            newspaper = article.find_element(by=By.CSS_SELECTOR, value="span").text

            # 새 탭 열기
            browser.execute_script("window.open(arguments[0]);", link)
            time.sleep(2)  # 페이지 로드 대기
            browser.switch_to.window(browser.window_handles[1])  # 새 탭으로 전환

            # 본문 텍스트 수집
            caas_body_element = browser.find_element(
                by=By.CSS_SELECTOR, value=".caas-body"
            )
            main = caas_body_element.text

            # published_at 가져오기
            try:
                published_at = browser.find_element(by=By.TAG_NAME, value="time").text
                # print("First published date:", published_at)
                if published_at:
                    published_at = convert_Yahoo_date_to_datetime(published_at)
            except Exception:
                published_at = ""

            # 관련 종목 수집
            # try:
            #     stock_element = browser.find_element(
            #         by=By.CSS_SELECTOR, value=".caas-xray-entity a"
            #     )
            #     stock_name = stock_element.text
            #     stock_url = stock_element.get_attribute("href")
            # except:
            #     # 요소가 존재하지 않으면 빈 문자열 할당
            #     stock_name = ""
            #     stock_url = ""

            # 데이터 저장
            data.append(
                SQLMODEL.NewsPaper(
                    title=title,
                    body=main,
                    summary="TEMP SUMMARY",
                    link=link,
                    link_hash=get_sha256_hash(link),
                    image=image,
                    source=newspaper,
                    published_at=published_at,
                )
            )

            # 새 탭 닫기
            browser.close()
            browser.switch_to.window(original_window)  # 원래 창으로 돌아오기

        except Exception as e:
            print(f"Error occurred: {e}")
            continue

    return data


def main():
    browser = setup_browser()
    browser.get("https://finance.yahoo.com/topic/stock-market-news/")
    scroll_page(browser)
    newspapers = scrape_articles(browser)
    try:
        upsert_newspapers(newspapers)
    except Exception as e:
        print("ERROR OCCURRED:", e)

    browser.quit()


main()
