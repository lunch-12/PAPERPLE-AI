# -*- coding: utf-8 -*- 
from gensim.summarization import summarize

# 예시 텍스트
text = """
중앙위 의결…18일 全大서 확정경선불복 → 공천불복 제재 확대더불어민주당은 12일 당 중앙위원회에서 ‘기본사회’와 ‘당원 중심주의’를 담은 강령 개정안을 채택한다. 기본사회는 이재명 전 대표의 대표적인 복지 정책이고, 당원 중심주의는 이 전 대표가 추구하는 새로운 정당의 모습이다. ‘경선 불복에 대한 제재’를 ‘공천 불복에 대한 제재’로 수정하는 내용 등을 담은 당헌 개정안도 중앙위에 오른다.민주당은 이날 중앙위 온라인 투표를 통해 ‘기본사회’ ‘당원 중심주의’를 명시한 강령 개정안을 의결한다. 이 개정안은 민주당 8·18 전국당원대회에서 최종 확정될 것으로 관측된다. 강령 개정안 전문에는 모든 사람이 공정하고 동등한 조건에서 역량을 발휘하는 ‘정의로운 나라’, 사회경제적 양극화·불평등을 극복하고 기본적인 삶을 보장하는 ‘기본사회’, 계층·세대·성별·지역 갈등을 해소하고 모든 국민의 조화로운 삶을 지향하는 ‘통합의 국가’ 등이 명시됐다. 더 강한 민주주의와 당원 중심 대중 정당을 목표로 당원 중심 정당 강화 방향을 구체화해야 한다는 내용도 담겼다. 강령 개정안이 전당대회를 거쳐 최종 확정되면 민주당 내 이 전 대표 체제가 한층 강화될 것으로 보인다.중앙위는 당헌 84조의 ‘선거부정 및 경선 불복에 대한 제재’를 ‘공천 불복에 대한 제재’로 수정하는 당헌 개정안도 의결한다. 민주당은 지난 6월 당헌 100조의 당내 경선 시 감산 대상을 기존 ‘경선 불복 경력자’에서 ‘공천 불복 경력자’로 개정했다. 다만 당내 일각에서는 후보자가 중앙당의 전략공천이나 컷오프(공천 배제) 결정에 항의할 수 있는 길을 차단하는 게 아니냐는 지적을 제기하고 있다."""

# 요약
summary = summarize(text, word_count=50)  # word_count는 요약 후 남을 단어 수를 설정합니다.
print(summary)

'''
import pandas as pd
from gensim.summarization import summarize

# 엑셀 파일 읽기
file_path = './data/article_df_240812.xlsx'
df = pd.read_excel(file_path)

# 상위 20개의 데이터만 선택
df_top20 = df.head(20)

# 요약된 문장을 저장할 새로운 열 생성
def safe_summarize(text):
    # 텍스트가 두 개 이상의 문장을 포함하고 있고, 단어 수가 50개 이상인지 확인
    if isinstance(text, str) and len(text.split('. ')) > 1 and len(text.split()) > 50:
        return summarize(text, word_count=50).split('. ')
    else:
        return []  # 조건을 만족하지 않으면 빈 리스트 반환

df_top20['summary'] = df_top20['main'].apply(safe_summarize)

# 요약된 데이터를 저장할 엑셀 파일 경로
output_file_path = './data/article_df_240812_summary_top20.xlsx'

# 엑셀 파일로 저장
df_top20.to_excel(output_file_path, index=False)

print(f"상위 20개의 요약된 데이터를 {output_file_path}에 저장했습니다.")
'''