import re
import pandas as pd
from openai import OpenAI
import requests
import json
import urllib.request

# OpenAI 클라이언트 설정
def setup_openai_client():
    return OpenAI(
        base_url='http://localhost:11434/v1',
        api_key='ollama',  # required, but unused
    )
# 엑셀 파일 읽기
def read_excel_file(file_path):
    return pd.read_excel(file_path)

# 뉴스 요약 및 관련 종목 추출
def get_related_stock(client, content):
    cleaned_content = content.replace('\n', ' ').replace('\r', '').strip()[:800]
    response = client.chat.completions.create(
        model="gemma2",  # llama3.1
        messages=[
            {"role": "system", "content": "다음 뉴스와 가장 관련있는 주식종목이름 1개만을 반환해라. 주식종목명만 반환. 만약 관련 종목이 없다면 ''을 반환하라"},
            {"role": "user", "content": cleaned_content}
        ]
    )
    return response.choices[0].message.content.strip()

# 종목 코드 찾기
def get_stock_code(stock, code_df):
    if stock != '':
        # 종목 이름을 소문자 또는 대문자로 비교하여 일치하는 행을 찾음
        matching_rows = code_df.loc[
            (code_df['name'].str.lower() == stock.lower()) | 
            (code_df['name'].str.upper() == stock.upper()), 
            'code'
        ]
        
        if not matching_rows.empty:
            return matching_rows.values[0]
    return None

# 종목 정보 가져오기
def fetch_stock_info(stock_code):
    if stock_code:
        url = f"https://m.stock.naver.com/api/stock/{stock_code}/integration"
        try:
            raw_data = urllib.request.urlopen(url).read()
            json_data = json.loads(raw_data)
            stock_name = json_data.get('stockName', 'N/A')
            current_price = json_data['dealTrendInfos'][0].get('closePrice', 'N/A')
            last_price_change = json_data['dealTrendInfos'][0].get('compareToPreviousClosePrice', 'N/A')
            return stock_name, current_price, last_price_change
        except Exception as e:
            print(f"Error fetching data for stock code {stock_code}: {e}")
    return 'N/A', 'N/A', 'N/A'

# 종목명 처리 및 정보 가져오기
def process_stock_info(stock, code_df, results, row):
    if stock:
        # 먼저 원래 이름으로 종목 코드 찾기 시도
        stock_code = get_stock_code(stock, code_df)

        # 추가 처리: 종목 코드가 아닌 경우 처리
        if not stock_code:
            # 1. '035420'와 같이 종목명이 종목코드로 반환된 경우
            if re.match(r'^\d{6}$', stock):
                stock_name, current_price, last_price_change = fetch_stock_info(stock)
                results.append({
                    '뉴스 제목': row['title'],
                    '관련 종목명': stock_name,
                    '종목 코드': stock,
                    '현재 가격': current_price,
                    '전일대비 등락가격': last_price_change
                })
                return

            # 2. '네이버(035420)'와 같이 종목명에 괄호로 종목 코드가 포함된 경우
            match = re.search(r'\((\d{6})\)', stock)
            if match:
                stock_code = match.group(1)
                stock_name, current_price, last_price_change = fetch_stock_info(stock_code)
                results.append({
                    '뉴스 제목': row['title'],
                    '관련 종목명': stock_name,
                    '종목 코드': stock_code,
                    '현재 가격': current_price,
                    '전일대비 등락가격': last_price_change
                })
                return

            # 3. '네이버(주)'와 같이 괄호 포함 텍스트를 제거한 후 다시 시도
            stock_name_cleaned = re.sub(r'\(.*?\)', '', stock).strip()
            stock_code = get_stock_code(stock_name_cleaned, code_df)
            if stock_code:
                stock_name, current_price, last_price_change = fetch_stock_info(stock_code)
                results.append({
                    '뉴스 제목': row['title'],
                    '관련 종목명': stock_name,
                    '종목 코드': stock_code,
                    '현재 가격': current_price,
                    '전일대비 등락가격': last_price_change
                })
                return

        # 종목 코드를 찾았을 경우 정보 가져오기
        if stock_code:
            stock_name, current_price, last_price_change = fetch_stock_info(stock_code)
            results.append({
                '뉴스 제목': row['title'],
                '관련 종목명': stock_name,
                '종목 코드': stock_code,
                '현재 가격': current_price,
                '전일대비 등락가격': last_price_change
            })
        else:
            results.append({
                '뉴스 제목': row['title'],
                '관련 종목명': stock,
                '종목 코드': 'N/A',
                '현재 가격': 'N/A',
                '전일대비 등락가격': 'N/A'
            })
            print(f"{stock}에 해당하는 국내종목코드를 찾을 수 없습니다.")
    else:
        print(f"해당 기사에서 관련종목을 못 찾았습니다.")
        results.append({
            '뉴스 제목': row['title'],
            '관련 종목명': 'N/A',
            '종목 코드': 'N/A',
            '현재 가격': 'N/A',
            '전일대비 등락가격': 'N/A'
        })

# 결과 저장
def save_results_to_excel(results, output_file):
    results_df = pd.DataFrame(results)
    results_df.to_excel(output_file, index=False)
    print(f"결과가 '{output_file}' 파일로 저장되었습니다.")

# 메인 함수
def main():
    client = setup_openai_client()
    
    # 뉴스 기사 데이터 읽기
    df = read_excel_file('./data/article_df_240812.xlsx')
    new_df = df.tail(20)

    # 한국거래소 종목 코드 데이터 읽기
    code_df = read_excel_file('data/국내상장법인.xlsx')

    results = []

    # 각 뉴스 기사에 대해 관련 종목 정보 가져오기
    for index, row in new_df.iterrows():
        stock = get_related_stock(client, row['main'])
        print('관련 종목명: ', stock)

        process_stock_info(stock, code_df, results, row)

    # 결과를 새로운 엑셀 파일로 저장
    save_results_to_excel(results, 'data/관련주식정보.xlsx')

if __name__ == "__main__":
    main()
