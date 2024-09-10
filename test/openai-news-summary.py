import logging
from dotenv import load_dotenv
import openai
import json
import os
from openai import OpenAI
import pandas as pd
import time


# OpenAI API 키 설정
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# 템플릿 문자열 정의
template_string = """
작업: 다음 기사의 내용을 면밀히 분석하여 가장 중요하고 관련성 높은 정보를 바탕으로 3줄 문장으로 요약하세요. 3가지 포인트를 추출하기에 정보가 충분하지 않다면, 추출할 수 있는 포인트는 기입하고 그 외에는 '정보불충분'이라고 적어주십시오. 각 포인트는 간결하게 한 문장으로 작성하되, 핵심 정보를 포함해야 합니다.

기사본문 내용: {text}
"""

def gpt_summarize(article_content):
    """
    해당 내용을 GPT API로 분석하여 요약하는 함수.

    Args:
        article_content (str): 기사 내용

    Returns:
        dict: 요약된 포인트를 포함한 결과 딕셔너리
    """
    # 템플릿 문자열을 대화 내용으로 완성
    prompt = template_string.format(text=article_content)

    try:
        start_time = time.time()  # 개별 요약 시작 시간 기록

        client = OpenAI(
            api_key=openai.api_key,
        )


        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4",  # 또는 "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # 응답 메시지를 추출
        customer_response = response.choices[0].message.content

        end_time = time.time()  # 개별 요약 종료 시간 기록
        elapsed_time = end_time - start_time
        logging.info(f"기사 요약 시간: {elapsed_time:.2f} 초")  # 개별 요약 시간 출력
        # # JSON 형식으로 파싱
        # output_dict = json.loads(customer_response)

        return customer_response

    except Exception as e:
        # 오류가 발생할 경우 로깅
        logging.error(f"OpenAI API 호출 중 오류 발생: {e}")
        return None
overall_start_time = time.time()
# 엑셀 파일 읽기
file_path = './data/article_df_240812.xlsx'
df = pd.read_excel(file_path)
df=df.tail(10)
# 'title'과 'main' 열을 결합하여 새로운 열 'content' 생성
df['content'] = df['title'] + "\n" + df['main']

# 'content' 열에 대해 gpt_summarize 함수를 적용하여 요약 결과 생성
df['summary'] = df['content'].apply(gpt_summarize)

# 기사별 요약 내용을 JSON으로 변환
articles_json = df[['title', 'main', 'summary']].to_dict(orient='records')

# JSON 데이터 출력
json_output = json.dumps(articles_json, ensure_ascii=False, indent=4)
# print(json_output)

# 전체 처리 시간 측정을 위한 종료 시간 기록
overall_end_time = time.time()
total_elapsed_time = overall_end_time - overall_start_time

# 전체 소요 시간 출력
print(f"전체 요약 처리 시간: {total_elapsed_time:.2f} 초")
