
# 국내 종목이름 입력시 종목코드 조회하기
import pandas as pd
import json
import requests
import urllib.request

# 현재 2024.8.26 기준 데이터 새로 갱신
# #한국거래소에서 종목 코드 받아옵니다. [0]은 헤더를 첫번째 행으로 지정하기 위해 사용
# url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
# response = requests.get(url)
# response.encoding = 'euc-kr'  # Specify the correct encoding

# # Parse the HTML content with pandas
# code_df = pd.read_html(response.text, header=0)[0]

# # Format 종목코드 to be 6 digits
# code_df['종목코드'] = code_df['종목코드'].map('{:06d}'.format)

# # Select only the necessary columns
# code_df = code_df[['회사명', '종목코드']]

# # Rename columns to English
# code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

# code_df.to_excel('data/test_data/국내상장법인.xlsx', index=False)
code_df=pd.read_excel('data/test_data/국내상장법인.xlsx', dtype={'code': str})

# Display the first few rows
print(code_df.head())
'''
        name    code
0     BGF리테일  282330
1      DRB동일  004840
2         E1  017940
3  HDC현대산업개발  294870
4  HD현대마린솔루션  443060
'''
stock='naver'
stock_code = code_df.loc[(code_df['name'].str.lower() == stock.lower()) | (code_df['name'].str.upper() == stock.upper()), 'code']

stock_code=code_df.loc[code_df['name'] == 'NAVER', 'code'].values[0]


#종목 코드
item_code = stock_code
url = "https://m.stock.naver.com/api/stock/%s/integration"%(item_code)
#https://m.stock.naver.com/domestic/stock/373220/total
#urllib.request를 통해 링크의 결과를 가져옵니다.
raw_data = urllib.request.urlopen(url).read()
#추후, 데이터 가공을 위해 json 형식으로 변경 합니다.
json_data = json.loads(raw_data)
#print(json_data)
#종목명 가져오기
stock_name = json_data['stockName']
print("종목명 : %s"%(stock_name))

#가격 가져오기
current_price = json_data['dealTrendInfos'][0]['closePrice']
print("가격 : %s"%(current_price))

#등락차 가져오기
deal = json_data['dealTrendInfos'][0]  # 가장 최근 날짜의 것을 가져옴

# compareToPreviousClosePrice 값 가져오기
if 'compareToPreviousClosePrice' in deal:
    last_price_change = deal['compareToPreviousClosePrice']  # 'text'에 해당 정보가 있음
    print("전일대비 등락가격:", last_price_change)

print()
# 관련 주식(동일 업종 비교)
# industryCompareInfo에서 각 종목에 대한 정보 가져오기
industry_comparison = json_data.get('industryCompareInfo', [])

for stock_info in industry_comparison[:3]:  # 상위 3개의 종목 정보만 가져오기
    stock_name = stock_info.get('stockName')
    compare_to_previous_close_price = stock_info.get('compareToPreviousClosePrice', {})
    close_price = stock_info.get('closePrice')
    
    print(f"종목명: {stock_name}")
    print(f"가격: {close_price}")
    print(f"전일대비 등락가격: {compare_to_previous_close_price}")
    print("-" * 30)
    
    