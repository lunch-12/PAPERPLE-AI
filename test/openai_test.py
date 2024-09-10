import logging
from dotenv import load_dotenv
import openai
import json
import os
from openai import OpenAI
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

        # # JSON 형식으로 파싱
        # output_dict = json.loads(customer_response)

        return customer_response

    except Exception as e:
        # 오류가 발생할 경우 로깅
        logging.error(f"OpenAI API 호출 중 오류 발생: {e}")
        return None

# 테스트 실행
article_text = '''동양생명 상반기 당기순이익 1753억원...보험손익 전년 比 17.8% 증가.
                    보장성 상품 APE 3875억원전년 比 23.2% 순증 
동양생명 제공 [파이낸셜뉴스] 동양생명이 보장성 상품 판매 호조에 따른 보험손익 성장에 힘입어 2024년 상반기 1753억원의 당기순이익을 시현했다고 12일 밝혔다.   먼저 보험손익은 보장을 강화해 출시하고 있는 건강 및 종신보험 등 보장성 상품의 지속적인 인기를 바탕으로 전년 동기 대비 17.8% 증가한 1368억원을 달성했다.   보험영업의 성장을 가능할 수 있는 상반기 연납화보험료(APE)는 전년동기대비 24% 증가한 4357억원을 기록했으며, 보장성 상품 APE는 3875억원으로 전년 동기 대비 23.2% 순증하는 등 보험영업과 보장성 보험 매출 모두에서 견고한 성장세를 보였다.   보험사의 장래 이익을 반영하는 지표인 신계약 계약서비스마진(CSM)은 상반기에 3435억원을 달성했으며, 이에 따라 상반기 CSM 잔액은 연초 대비 8.3% 증가한 2조7000억원을 기록했다.   이번 실적은 동양생명의 다양한 판매 채널의 균형잡힌 성장을 바탕으로 시현됐으며, 특히 전속조직인 FC채널은 보장성 APE에서 전년 동기 대비 약 61.3% 증가한 높은 성장세를 보여주었다.   또 효율관리 노력을 바탕으로 보장성 보험에 대한 13회차(88.5%)와 25회차(68%) 유지율은 지속적으로 개선되고 있으며, 투자손익은 시장변동성 관리 강화와 안정성에 중점을 둔 선별적인 투자 등을 바탕으로 872억원을 기록했다.   동양생명 관계자는 “올 상반기에는 공동재보험을 통해 자본관리 선진화의 기반을 마련했으며, 데이터 관리체계 고도화와 마이엔젤서비스 통합 구축 등을 통해 효율성장 기반 또한 마련했다”며 “하반기에도 고객 건강과 행복을 지키는 수호천사가 될 수 있도록, 영업 활성화를 기반으로 지속가능한 수익구조 확보와 보유이원 제고를 통한 안정적인 투자 손익 창출 그리고 자본 건전성 강화를 위해 최선을 다할 것”이라고 말했다.'''
result = gpt_summarize(article_text)
print(result)
