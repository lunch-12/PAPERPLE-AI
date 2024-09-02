import json
import urllib.request

#종목 코드
item_code ="XRP"
url = f'https://m.stock.naver.com/front-api/crypto/otherExchange?nfTicker={item_code}&excludeExchange=UPBIT'


#urllib.request를 통해 링크의 결과를 가져옵니다.
raw_data = urllib.request.urlopen(url).read()
#추후, 데이터 가공을 위해 json 형식으로 변경 합니다.
json_data = json.loads(raw_data)
#print(json_data)

# 종목명 가져오기
# JSON 구조에 따라 적절히 접근하여 krName, tradePrice, changeValue를 추출합니다.
if json_data['isSuccess']:
    item = json_data['result'][0]
    stock_name = item['krName']
    trade_price = item['tradePrice']
    change_value = item['changeValue']
    
    print(f"종목명: {stock_name}")
    print(f"가격 : {trade_price}")
    print(f"변동값: {change_value}")
else:
    print("데이터를 가져오는 데 실패했습니다.")

        