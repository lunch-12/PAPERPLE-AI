import re
import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

# Spacy 모델을 함수 외부에서 로드
nlp = spacy.load('en_core_web_sm')

def spacy_summarize(text, per):
    doc = nlp(text)
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS) and word.text.lower() not in punctuation:
            word_frequencies[word.text] = word_frequencies.get(word.text, 0) + 1
    
    max_frequency = max(word_frequencies.values())
    word_frequencies = {word: freq / max_frequency for word, freq in word_frequencies.items()}
    
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word.text.lower()]
    
    select_length = int(len(sentence_tokens) * per)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    return summary.strip()

def clean_text(text):
    # 1. 'YYYY.MM.DD' 형태의 날짜 패턴 제거
    text = re.sub(r'\d{4}\.\d{1,2}\.\d{1,2}', '', text)
    
    # 2. '재판매 및 DB 금지' 텍스트 제거
    text = re.sub(r'재판매 및 DB 금지', '', text)
    
    # 3. '@'가 포함된 텍스트 제거
    text = re.sub(r'\S*@\S*\s?', '', text)

    # 4. '~ 기자' 패턴 제거
    text = re.sub(r'\S* 기자', '', text)

    # 5. 괄호 안에 '사진', '뉴스', '제공'이 포함된 경우 괄호와 내용 제거
    text = re.sub(r'\(.*?(사진|제공).*?\)', '', text)  # 소괄호
    text = re.sub(r'\[.*?(사진|제공).*?\]', '', text)  # 대괄호
    text = re.sub(r'\{.*?(사진|제공).*?\}', '', text)  # 중괄호

    # 6. '<사진=디즈니>' 와 같은 패턴 제거
    text = re.sub(r'<.*?>', '', text)
    
    # 7. '[이데일리 김윤지 기자]' 와 같이 '[ ]' 형태 제거 및 안에 텍스트 모두 제거
    text = re.sub(r'\[.*?\]', '', text)
    
    # 8. '<AFP연합뉴스>'와 같은 패턴 제거
    text = re.sub(r'<.*?\>', '', text)

    # 9. '<AFP연합뉴스>'와 같은 패턴 제거
    text = re.sub(r'【.*?\】', '', text)

    # 10. 특수기호 삭제
    text = re.sub(r'Q.', 'Q', text)
    
    text = re.sub(r'\.\s*\.', '.', text)
    text = re.sub(r'[ⓒ▲◆▶▷■\[\]=+\#/\?^@*※~!△☞◀━-]', '', text)

    # 11. 여러 개의 탭(\t), 줄바꿈(\n), 공백을 하나의 공백으로 대체
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


# 엑셀 파일 읽기
file_path = './data/article_df_240812.xlsx'
df = pd.read_excel(file_path)
df_top20=df.head(20)
# 요약된 문장을 저장할 새로운 열 생성
df_top20['cleaned_main'] = df_top20['main'].apply(clean_text)
# 최대 100자(DB기준 VAR(225))
df_top20['summary'] = df_top20['cleaned_main'].apply(lambda x: spacy_summarize(x, 0.1))  # 10% 요약

# summary 열을 '.' 기준으로 줄바꿈하여 저장
df_top20['summary'] = df_top20['summary'].apply(lambda x: x.replace('. ', '.\n'))

# 요약된 데이터를 저장할 엑셀 파일 경로
output_file_path = './data/test_data/article_df_240821_spaCy_summary_top20.xlsx'

# 엑셀 파일로 저장
df_top20.to_excel(output_file_path, index=False)

print(f"요약된 데이터를 {output_file_path}에 저장했습니다.")