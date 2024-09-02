# 주식 투자 사이트에서 검색쿼리 과정을 통해 주식정보를 가져온다.

#https://www.investing.com/search/?q=Japan%20Airlines
item_code ="XRP"
# url = f'https://www.investing.com/search/?q={item_code}'

#쿼리검색 > 최상단 주식링크로 연결
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# Chrome 드라이버 설정
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


chrome_options = Options()
chrome_options.add_argument("--headless")  # 브라우저 창을 열지 않음
service = Service(executable_path='path_to_chromedriver')  # chromedriver의 경로를 설정

# 웹 드라이버 시작
driver = setup_browser()

# 첫 번째 단계: 검색 URL로 이동
search_url = 'https://www.investing.com/search/?q=coupang'
driver.get(search_url)

# 첫 번째 href 속성 가져오기 (동적 요소가 아닌 경우)
first_a_tag = driver.find_element(By.CLASS_NAME, 'js-inner-all-results-quote-item.row')
href = first_a_tag.get_attribute('href')

print(href)
# 두 번째 단계: href 링크로 이동
driver.get(href)

# 필요한 동적 요소를 기다린 후 가져오기
driver.implicitly_wait(10)  # 최대 10초 동안 요소가 나타나기를 기다림

# 첫 번째 h1 태그의 텍스트 가져오기
first_target_tag = driver.find_element(By.CLASS_NAME, 'mb-2.5.text-left.text-xl.font-bold.leading-7.text-[#232526].md:mb-2.md:text-3xl.md:leading-8.rtl:soft-ltr')
print("첫 번째 요소의 텍스트:")
print(first_target_tag.text)