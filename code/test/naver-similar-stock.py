import json
import urllib.request

#종목 코드
item_code = "373220"
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

