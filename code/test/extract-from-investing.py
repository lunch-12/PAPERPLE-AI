# 주식 투자 사이트에서 검색쿼리 과정을 통해 주식정보를 가져온다.

#https://www.investing.com/search/?q=Japan%20Airlines
item_code ="XRP"
# url = f'https://www.investing.com/search/?q={item_code}'

#쿼리검색 > 최상단 주식링크로 연결
import requests
from bs4 import BeautifulSoup

# 첫 번째 단계: 첫 번째 href 속성 가져오기
search_url = 'https://www.investing.com/search/?q=coupang'
response = requests.get(search_url)
soup = BeautifulSoup(response.content, 'html.parser')

# 클래스명이 'js-inner-all-results-quotes-wrapper newResultsContainer quatesTable'인 div 내부의 첫 번째 a 태그 찾기
wrapper = soup.find('div', class_='js-inner-all-results-quotes-wrapper newResultsContainer quatesTable')
first_a_tag = wrapper.find('a', class_='js-inner-all-results-quote-item row') if wrapper else None

# 두 번째 단계: 첫 번째 href 링크로 이동하여 필요한 텍스트 추출
if first_a_tag:
    href = first_a_tag['href']
    full_url = 'https://www.investing.com' + href
    print(full_url)
    detail_response = requests.get(full_url)
    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

    # 종목 텍스트 가져오기
    target_tag = detail_soup.find('h1', class_='mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr')

    if target_tag:
        print(target_tag.get_text())
    else:
        print("지정된 클래스명을 가진 태그를 찾을 수 없습니다.")
else:
    print("첫 번째 href 링크를 찾을 수 없습니다.")

    
    
