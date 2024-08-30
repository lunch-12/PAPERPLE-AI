# 데이터를 가져오기 위한 요청
import urllib.request
import json

# 원하는 인덱스 코드
index_code = "AAPL"
index_code += ".O"

# URL 생성
url = f"https://api.stock.naver.com/stock/{index_code}/basic"


try:
    #urllib.request를 통해 링크의 결과를 가져옵니다.
    raw_data = urllib.request.urlopen(url).read()
    #추후, 데이터 가공을 위해 json 형식으로 변경 합니다.
    json_data = json.loads(raw_data)
    #print(json_data)
    #종목명 가져오기
    stock_name = json_data['stockName']
    print("종목명 : %s"%(stock_name))

    #가격 가져오기
    current_price = json_data['closePrice']
    print("가격 : %s"%(current_price))

    #등락차 가져오기
    last_price_change = json_data['compareToPreviousClosePrice']  # 'text'에 해당 정보가 있음
    print("전일대비 등락가격:", last_price_change)

except Exception as e:
    print(f"Error fetching data for index {index_code}: {e}")

