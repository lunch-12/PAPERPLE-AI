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

#시총 가져오기
for code in json_data['totalInfos']:
    if 'marketValue' == code['code']:
        marketSum_value = code['value']
        print("시총 : %s"%(marketSum_value))

#PER 가져오기
for i in json_data['totalInfos']:
    if 'per' == i['code']:
        per_value_str = i['value']
        print("PER : %s"%(per_value_str))


#PBR 가져오기
for v in json_data['totalInfos']:
    if 'pbr' == v['code']:
        pbr_value_str = v['value']
        print("PBR : %s"%(pbr_value_str))
        