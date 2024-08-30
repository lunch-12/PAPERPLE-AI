import re
import pandas as pd
from openai import OpenAI
import json
import urllib.request
from kakaotrans import Translator


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
            {"role": "system", "content": "다음 뉴스와 가장 관련있는 주식종목이름 1개만을 반환해라. 주식종목명만 반환. 만약 관련 종목이 없다면 'N/A'만을 반환하라"},
            {"role": "user", "content": cleaned_content}
        ]
    )
    return response.choices[0].message.content.strip()

# 종목 코드 찾기
def get_stock_code(stock, code_df):
    if stock != 'N/A':
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

# 정보 저장
def fetch_and_append_stock_info(stock_code, row, results):
    stock_name, current_price, last_price_change = fetch_stock_info(stock_code)
    results.append({
        '뉴스 제목': row['title'],
        '관련 종목명': stock_name,
        '종목 코드': stock_code,
        '현재 가격': current_price,
        '전일대비 등락가격': last_price_change
    })
    
    
# 종목명 처리 및 정보 가져오기
def process_stock_info(stock, code_df, results, row):
    if stock != 'N/A':
        # 먼저 원래 이름으로 종목 코드 찾기 시도
        stock_code = get_stock_code(stock, code_df)

        # 추가 처리: 종목 코드가 아닌 경우 처리
        if not stock_code:
            # 1. '035420'와 같이 종목명이 종목코드로 반환된 경우
            if re.match(r'^\d{6}$', stock):
                fetch_and_append_stock_info(stock, row, results)
                return

            # 2. '네이버(035420)'와 같이 종목명에 괄호로 종목 코드가 포함된 경우
            match = re.search(r'\((\d{6})\)', stock)
            if match:
                stock_code = match.group(1)
                fetch_and_append_stock_info(stock_code, row, results)
                return

            # 3. 'SS0IAQ (삼성전자)'와 같이 괄호로 종목명이 포함된 경우
            match = re.search(r'\((.*?)\)', stock)
            if match:
                stock_name = match.group(1)  # 괄호 안의 종목명 추출
                stock_code = get_stock_code(stock_name, code_df)
                if stock_code:
                    fetch_and_append_stock_info(stock_code, row, results)
                    return
            
            # 4. '네이버(주)'와 같이 괄호 포함 텍스트를 제거한 후 다시 시도
            stock_name_cleaned = re.sub(r'\(.*?\)', '', stock).strip()
            stock_code = get_stock_code(stock_name_cleaned, code_df)
            if stock_code:
                fetch_and_append_stock_info(stock_code, row, results)
                return

            stock = re.sub(r'\(.*?\)', '', stock).strip()
            
            # 5. 영어 알파벳이 포함된 경우 한글로 변환 후 다시 시도(nc소프트-->엔씨소프트)
            stock_translated = simple_filter(stock)
            if stock_translated != stock:  # 변환된 텍스트가 있을 경우
                stock_code = get_stock_code(stock_translated, code_df)
                if stock_code:
                    fetch_and_append_stock_info(stock_code, row, results)
                    return
                
            # 6. 영어 고유명을 한글로 변환(ncsoft-->엔씨소프트)
            stock_translated_2 = convert_english_name_to_korean(stock)
            if stock_translated_2 != stock:  # 변환된 텍스트가 있을 경우
                stock_code = get_stock_code(stock_translated_2, code_df)
                if stock_code:
                    fetch_and_append_stock_info(stock_code, row, results)
                    return
            

        # 종목 코드를 찾았을 경우 정보 가져오기
        if stock_code:
            fetch_and_append_stock_info(stock_code, row, results)
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

# 'NC소프트' >> '엔씨소프트'
def simple_filter(input_text):
    ENGS = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', 'g', 'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k',
            'K', 'l', 'L',
            'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w',
            'W', 'x', 'X', 'y', 'Y', 'z', 'Z']

    KORS = ['에이', '에이', '비', '비', '씨', '씨', '디', '디', '이', '이', '에프', '에프', '쥐', '쥐', '에이치', '에이치', '아이', '아이', '제이',
            '제이',
            '케이', '케이', '엘', '엘', '엠', '엠', '엔', '엔', '오', '오', '피', '피', '큐', '큐', '알', '알', '에스', '에스', '티', '티', '유',
            '유', '브이', '브이',
            '더블유', '더블유', '엑스', '엑스', '와이', '와이', '지', '지']

    trans = dict(zip(ENGS, KORS)) # 영어와 한글을 대칭하여 딕셔너리화
    # 변환된 결과를 저장할 리스트
    result_trans = []
    
    # input_text의 각 문자에 대해
    for char in input_text:
        if char in trans:  # 문자가 영어 알파벳인 경우
            result_trans.append(trans[char])  # 대응되는 한글 발음 추가
        else:
            result_trans.append(char)  # 영어 알파벳이 아닌 경우 원래 문자 그대로 추가
    
    # 결과 문자열로 합치기
    return ''.join(result_trans)


# NCsoft->엔씨소프트
# 영어 고유명을 한글로 변환
def convert_english_name_to_korean(name):
    
    name=name.replace(" ",'').upper()
    name_mapping = {
        "NCSOFT": "엔씨소프트",
        "SAMSUNG": "삼성전자",
        "삼성": "삼성전자",
        "LS전선": "LS",
        "NETMARBLE": "넷마블",
        # 필요에 따라 더 추가
    }
    
    # 매핑된 이름이 있으면 반환, 없으면 음역 적용
    if name in name_mapping:
        return name_mapping[name]
    
    translator = Translator()
    
    stock_korean_translated=translator.translate(name, src='en', tgt='kr')

    # stock_korean_translated이 여전히 영어만 아래있는 것들 중 매칭
    return stock_korean_translated
    
    
# 메인 함수
def main():
    client = setup_openai_client()
    
    # 뉴스 기사 데이터 읽기
    df = read_excel_file('./data/article_df_240812.xlsx')
    new_df = df.tail(100)

    # 한국거래소 종목 코드 데이터 읽기
    code_df = read_excel_file('data/국내상장법인.xlsx')

    results = []

    # 각 뉴스 기사에 대해 관련 종목 정보 가져오기
    for index, row in new_df.iterrows():
        stock = get_related_stock(client, row['title']+'.'+row['main'])
        print('관련 종목명: ', stock)

        process_stock_info(stock, code_df, results, row)

    # 결과를 새로운 엑셀 파일로 저장
    save_results_to_excel(results, 'data/관련주식정보_top100.xlsx')

if __name__ == "__main__":
    main()
