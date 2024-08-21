# -*- coding: utf-8 -*-
import re
import pandas as pd
from openai import OpenAI
from tqdm import tqdm  # tqdm 라이브러리 임포트

# OpenAI 클라이언트 설정
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',  # required, but unused
)

# 엑셀 파일 읽기
df = pd.read_excel('./data/article_df_240812.xlsx')

# 요약된 내용을 담을 리스트 생성
summaries = []
new_df=df.head(20)
# 'main' 컬럼의 각 문장에 대해 줄바꿈 제거, 800자 내로 자르고 요약 수행
# tqdm을 사용하여 진행 상황 표시
for content in tqdm(new_df['main'], desc="Processing"):
    # 줄바꿈 제거 및 300자 내로 자르기
    cleaned_content = content.replace('\n', ' ').replace('\r', '').strip()[:800]

    response = client.chat.completions.create(
        model="gemma",
        messages=[
            {"role": "system", "content": "다음 내용을 간략한 3줄 리스트로 요약해라. 줄바꿈은 한번만 해라"},
            {"role": "user", "content": cleaned_content}
        ]
    )
    # 요약된 내용을 리스트에 추가
    summary = response.choices[0].message.content
    summary = re.sub(r'\s*\n\s*', '\n', summary)  # 여러 줄바꿈을 하나로
    summaries.append(summary)

# 새로운 컬럼 'summary'에 요약된 내용 추가
new_df['summary'] = summaries

# 결과를 새로운 엑셀 파일로 저장
new_df.to_excel('./data/article_df_240816_with_summaries.xlsx', index=False)

print("요약이 완료되고 새로운 파일이 저장되었습니다.")
