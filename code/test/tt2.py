import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# 크롬 드라이버 생성
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Google 웹사이트에 접속
driver.get("https://www.google.com")

# 검색 입력창 찾기 (검색창의 이름이 'q')
search_box = driver.find_element(By.NAME, 'q')

# 검색어 입력
stock='samsung电子'
search_box.send_keys(f'{stock} 주식')

# 검색 실행
search_box.submit()
time.sleep(1)
# 결과 페이지 스크린샷 저장

# 이후 작업: 예를 들어, 첫 번째 검색 결과의 링크를 클릭하기
try:
    # 주어진 클래스명을 가진 <div> 요소를 찾기
    first_result = driver.find_element(By.CSS_SELECTOR, 'div.PZPZlf.ssJ7i.B5dxMb')

    # 해당 요소의 텍스트 가져오기
    result_text = first_result.text

    # 검색된 텍스트 출력
    print("종목 이름:", result_text) #samsung

    # 필요한 추가 작업 수행...
    second_result = driver.find_element(By.CSS_SELECTOR, 'div.iAIpCb.PZPZlf')
    
    # 해당 요소의 텍스트 가져오기
    result_text = second_result.text
    cleaned_text = result_text.split(":")[1].strip()
    
    # 검색된 텍스트 출력
    print("종목 코드:", cleaned_text) 
    
    third_result = driver.find_element(By.CSS_SELECTOR, 'span[jsname="vWLAgc"]') #IsqQVc NprOob wT3VGc
    
    # 해당 요소의 텍스트 가져오기
    result_text = third_result.text
    
    # 검색된 텍스트 출력 
    print("가격:", result_text) 
    
    fourth_result = driver.find_element(By.CSS_SELECTOR, 'span[jsname="qRSVye"]')
    
    # 해당 요소의 텍스트 가져오기
    result_text = fourth_result.text
    
    # 검색된 텍스트 출력
    print("등락차:", result_text) 
    
except Exception as e:
    print(f"해당 종목이 검색이 안됨: {e}")

# 브라우저 닫기
driver.quit()