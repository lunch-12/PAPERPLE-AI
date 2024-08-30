# 데이터를 가져오기 위한 요청
import urllib.request
import json

# 원하는 인덱스 코드
index_code = "AMZN.O"

# URL 생성
industry_comparison_url='https://api.stock.naver.com/stock/{index_code}/integration'


try:
    # industryCompareInfo에서 각 종목에 대한 정보 가져오기
    #urllib.request를 통해 링크의 결과를 가져옵니다.
    raw_data = urllib.request.urlopen(industry_comparison_url).read()
    #print(raw_data)
    #추후, 데이터 가공을 위해 json 형식으로 변경 합니다.
    global_data = json.loads(raw_data)
    # # 관련 주식(동일 업종 비교)
    # '''
    # "reutersCode": "COST.O",
    # "symbolCode": "COST",
    # "stockName": "코스트코 홀세일"
    # '''
    # globalStocks 리스트 내의 stockName, closePrice, compareToPreviousClosePrice를 가져오기
    global_stocks = global_data['industryCompareInfo']['globalStocks'][:3]

    # 모든 stockName, closePrice, compareToPreviousClosePrice를 출력
    for stock in global_stocks:
        stock_name = stock['stockName']
        close_price = stock['closePrice']
        compare_price = stock['compareToPreviousClosePrice']
        print(f"종목명: {stock_name}")
        print(f"가격: {close_price}")
        print(f"전일대비 등락가격: {compare_price}")
        print("-" * 30)
        
except Exception as e:
    print(f"Error fetching data for index {index_code}: {e}")

