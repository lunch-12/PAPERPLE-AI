# -*- coding: utf-8 -*-
import pandas as pd
from openai import OpenAI

# OpenAI 클라이언트 설정
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',  # required, but unused
)

# 엑셀 파일 읽기 (앞 10줄만 가져오기)
df = pd.read_excel('./data/article_df_240812.xlsx').head(1)

# 요약된 내용을 담을 리스트 생성
summaries = []

# 'main' 컬럼의 각 문장에 대해 줄바꿈 제거, 300자 내로 자르고 요약 수행
for content in df['main']:
    # 줄바꿈 제거 및 800자 내로 자르기
    cleaned_content = content.replace('\n', ' ').replace('\r', '').strip()[:800]
    print('--------------------')
    print("<원 문장>")
    print('--------------------')
    print(cleaned_content)
    response = client.chat.completions.create(
        model="gemma",
        messages=[
            {"role": "system", "content": "다음 내용을 간략한 3줄 리스트로 요약해라. 줄바꿈은 한번만 해라"},
            {"role": "user", "content": cleaned_content}
        ]
    )
    # 요약된 내용을 리스트에 추가
    summary = response.choices[0].message.content
    print('--------------------')
    print("<요약 내용>")
    print('--------------------')
    print(summary)
    summaries.append(summary)

# 새로운 컬럼 'summary'에 요약된 내용 추가
# df['summary'] = summaries

# # 결과를 새로운 엑셀 파일로 저장
# df.to_excel('article_df_240812_with_summaries_top10.xlsx', index=False)
new_df=df.head(10)
new_df['summary']=summaries
new_df.to_excel('article_df_240812_with_summaries_top10.xlsx', index=False)
print("앞 10줄 요약이 완료되고 새로운 파일이 저장되었습니다.")
