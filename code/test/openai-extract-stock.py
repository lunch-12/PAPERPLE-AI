from dotenv import load_dotenv
import openai
import json
import os
from openai import OpenAI
import pandas as pd
import time
import ssl
import urllib.request

# OpenAI API 키 설정
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# 템플릿 문자열 정의
template_string = """
작업: 다음 기사 내용과 가장 관련있는 주식 종목 1개 이름과 종목 코드를 반환해라. 추출하기에 정보가 충분하지 않다면, '정보불충분'이라고 적어줘라. 이유는 적지마.

관련 종목명:  해당 종목의 이름을 반환

종목 코드: 해당 종목의 코드를 반환

기사본문 내용: {text}
"""

def extract_stock(article_content): #100개에 80초
    """

    Args:
        article_content (str): 기사 내용
    return:
        종목 코드: 정보불충분
        관련 종목명: 삼성전자
    """
    # 템플릿 문자열을 대화 내용으로 완성
    prompt = template_string.format(text=article_content)

    try:
        client = OpenAI(
            api_key=openai.api_key,
        )

        # OpenAI ChatGPT API를 호출하여 응답 받기
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. "},
                {"role": "user", "content": prompt}
            ],
        )

        # 응답 메시지를 추출
        customer_response = response.choices[0].message.content
        customer_response = customer_response.replace('\n\n', '\n')
        print(customer_response)
        print()
        return customer_response

    except Exception as e:
        # 오류가 발생할 경우 로깅
        logging.error(f"OpenAI API 호출 중 오류 발생: {e}")
        return '정보불충분'

# 한국 종목 정보 가져오기
def fetch_korean_stock_info(stock_code):
    if stock_code:
        url = f"https://m.stock.naver.com/api/stock/{stock_code}/integration"

        try:
            # SSL 인증서 무시 설정 (필요한 경우)
            context = ssl._create_unverified_context()

            # User-Agent 헤더 추가
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            req = urllib.request.Request(url, headers=headers)

            # URL 열기
            raw_data = urllib.request.urlopen(req, context=context).read()

            # JSON 데이터 파싱
            json_data = json.loads(raw_data)
            stock_name = json_data.get('stockName', 'N/A')
            current_price = json_data['dealTrendInfos'][0].get('closePrice', 'N/A')
            last_price_change = json_data['dealTrendInfos'][0].get('compareToPreviousClosePrice', 'N/A')
            return stock_name, current_price, last_price_change

        except Exception as e:
            print(f"{stock_code}에 해당하는 국내 종목 코드를 찾을 수 없습니다. 오류: {e}")

    return 'N/A', 'N/A', 'N/A'

# 외국 종목 및 가상자산 정보 가져오기
def fetch_foreign_or_crypto_stock_info(stock_code):
    stock_code=stock_code.upper()
    base_url = "https://api.stock.naver.com/stock/"
    index_codes = [
        f"{stock_code}.O",  # 예: NASDAQ (예: AAPL.O)
        f"{stock_code}.K",  # 예: 뉴욕거래소 (예: AAPL.K)
        stock_code,         # 기본 종목 코드 (예: AAPL)
        f".{stock_code}",   # 그 외 (예: .AAPL)
        f"{stock_code}.HM"  # 베트남 (예: AAPL.HM)
    ]

    for index_code in index_codes:
        url = f"{base_url}{index_code}/basic"
        
        try:
            # SSL 인증서 무시 설정 (필요한 경우)
            context = ssl._create_unverified_context()

            # User-Agent 헤더 추가
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            
            raw_data = urllib.request.urlopen(url).read()
            json_data = json.loads(raw_data)
            
            # 필요한 정보 추출
            stock_name = json_data.get('stockName', 'N/A')
            current_price = json_data.get('closePrice', 'N/A')
            last_price_change = json_data.get('compareToPreviousClosePrice', 'N/A')
            
            # 유효한 응답을 받으면 반환
            return stock_name, current_price, last_price_change
        except Exception as e:
            print(f"{index_code}에 해당하는 해외종목코드를 찾을 수 없습니다.")
    
    url = f'https://m.stock.naver.com/front-api/crypto/otherExchange?nfTicker={stock_code}&excludeExchange=UPBIT'
    try:
        raw_data = urllib.request.urlopen(url).read()
        json_data = json.loads(raw_data)
        if json_data['isSuccess']:
            item = json_data['result'][0]
            stock_name = item['krName']
            trade_price = item['tradePrice']
            change_value = item['changeValue']
            return stock_name, trade_price, change_value
        else:
            print(f"{stock_code}에 해당하는 가상자산 데이터를 가져오는 데 실패했습니다.")
    except Exception as e:
        print(f"{stock_code}에 해당하는 가상자산을 찾을 수 없습니다.")
    
    return 'N/A', 'N/A', 'N/A'

# 주식 정보 가져오기
def fetch_and_append_stock_info(stock_name, stock_code, row, results):
    # 국내 종목 처리
    if stock_code.isdigit():
        stock_name, current_price, last_price_change = fetch_korean_stock_info(stock_code)
    else:
        # 해외 종목 처리
        stock_name, current_price, last_price_change = fetch_foreign_or_crypto_stock_info(stock_code)

    results.append({
        '뉴스 제목': row['title'],
        '관련 종목명': stock_name,
        '종목 코드': stock_code,
        '현재 가격': current_price,
        '전일대비 등락가격': last_price_change
    })

# 종목 정보 처리 및 엑셀 저장
def process_and_save_stock_info(df):
    results = []

    # 기사별로 종목 추출 및 주식 정보 가져오기
    for _, row in df.iterrows():
        stock_info = extract_stock(row['content']).replace('\n\n', '\n').strip()
        
        # 종목 정보가 '정보불충분'이 아닌 경우 처리
        if '정보불충분' not in stock_info:
            # '관련 종목명: 종목 이름\n종목 코드: 종목 코드' 형식의 데이터를 처리
            stock_data = stock_info.split('\n')
            
            # 종목명과 종목코드 추출
            stock_name = stock_data[0].split(":")[1].strip()  # '관련 종목명' 처리
            stock_code = stock_data[1].split(":")[1].strip()  # '종목 코드' 처리

            # 종목 정보 가져와서 results에 저장
            fetch_and_append_stock_info(stock_name, stock_code, row, results)
        else:
            # '정보불충분'인 경우 처리
            results.append({
                '뉴스 제목': row['title'],
                '관련 종목명': '정보불충분',
                '종목 코드': '정보불충분',
                '현재 가격': 'N/A',
                '전일대비 등락가격': 'N/A'
            })

    # 결과반환

    return results

def main():
    overall_start_time = time.time()

    # 엑셀 파일에서 데이터 읽기
    file_path = './data/article_df_240812.xlsx'
    df = pd.read_excel(file_path)
    df = df.tail(100)

    # 'title'과 'main' 열을 결합하여 새로운 열 'content' 생성
    df['content'] = df['title'] + "\n" + df['main']

    # 종목 정보 처리
    results = process_and_save_stock_info(df)

    # 결과를 DataFrame으로 변환
    results_df = pd.DataFrame(results)

    # 결과 엑셀 파일로 저장
    output_file_path = './data/article_df_with_stock_info.xlsx'
    results_df.to_excel(output_file_path, index=False)
    print(f"종목 정보를 포함한 데이터를 {output_file_path}에 저장했습니다.")

    # 전체 처리 시간 기록
    overall_end_time = time.time()
    total_elapsed_time = overall_end_time - overall_start_time
    print(f"총 처리 시간: {total_elapsed_time:.2f} 초") #100개 기준 80초
    
if __name__ == "__main__":
    main()