from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Google에서 검색하여 종목명, 종목 코드, 가격, 등락차 가져오기
def fetch_stock_info_from_google(stock):
    start_time = time.time()  # 시작 시간 기록

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    # 구글 검색 URL로 접속
    driver.get(f'https://www.google.com/search?q={stock}+주식')

    # 페이지 로드 대기 (time.sleep 대신 WebDriverWait 사용하여 속도 개선)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.PZPZlf.ssJ7i.B5dxMb'))
        )
    except Exception as e:
        print(f"페이지 로딩 오류: {e}")
        driver.quit()
        return None

    try:
        # 종목 이름 가져오기
        stock_name_element = driver.find_element(By.CSS_SELECTOR, 'div.PZPZlf.ssJ7i.B5dxMb')
        stock_name = stock_name_element.text
    except Exception as e:
        stock_name = '종목명 불러오기 실패'
        print(f"Error: {e}")

    try:
        # 종목 코드 가져오기
        stock_code_element = driver.find_element(By.CSS_SELECTOR, 'div.iAIpCb.PZPZlf')
        stock_code = stock_code_element.text.split(":")[1].strip()
    except Exception as e:
        stock_code = '종목코드 불러오기 실패'
        print(f"Error: {e}")

    try:
        # 현재 가격 가져오기
        current_price_element = driver.find_element(By.CSS_SELECTOR, 'span[jsname="vWLAgc"]')
        current_price = current_price_element.text
    except Exception as e:
        current_price = '가격 불러오기 실패'
        print(f"Error: {e}")

    try:
        # 등락차 가져오기
        last_price_change_element = driver.find_element(By.CSS_SELECTOR, 'span[jsname="qRSVye"]')
        last_price_change = last_price_change_element.text
    except Exception as e:
        last_price_change = '등락차 불러오기 실패'
        print(f"Error: {e}")

    # 브라우저 닫기
    driver.quit()

    # 실행 시간 측정
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"실행 시간: {execution_time:.2f} 초")

    return stock_name, stock_code, current_price, last_price_change

# 테스트 실행
result = fetch_stock_info_from_google('samsung 电子')
print(result)
