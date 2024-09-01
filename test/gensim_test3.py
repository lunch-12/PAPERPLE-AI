import re
import pandas as pd
import numpy as np
from konlpy.tag import Kkma, Twitter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import normalize

# 꼬꼬마 분석기 및 트위터 형태소 분석기 초기화
kkma = Kkma()
twitter = Twitter()

# 자연어처리 함수 정의
def text2sentences(text):
    sentences = kkma.sentences(text)
    for idx in range(0, len(sentences)):
        if len(sentences[idx]) <= 10:
            sentences[idx-1] += (' ' + sentences[idx])
            sentences[idx] = ''
    return sentences

def get_nouns(sentences):
    stopwords = ['머니투데이', '연합뉴스', '연합 뉴스', '데일리', '동아일보', '중앙일보', '조선일보', '기자', '아', '휴', 
                 '아이구', '아이쿠', '아이고', '어', '나', '우리', '저희', '따라', '의해', '을', '를', '에', '의', '가']
    nouns = []
    for sentence in sentences:
        if sentence != '':
            nouns.append(' '.join([noun for noun in twitter.nouns(str(sentence))
                                   if noun not in stopwords and len(noun) > 1]))
    return nouns

def build_sent_graph(sentence):
    tfidf = TfidfVectorizer()
    tfidf_mat = tfidf.fit_transform(sentence).toarray()
    graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
    return graph_sentence

def build_words_graph(sentence):
    cnt_vec = CountVectorizer()
    cnt_vec_mat = normalize(cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
    vocab = cnt_vec.vocabulary_
    return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word]: word for word in vocab}

def get_ranks(graph, d=0.85):
    A = graph
    matrix_size = A.shape[0]
    for id in range(matrix_size):
        A[id, id] = 0
        link_sum = np.sum(A[:, id])
        if link_sum != 0:
            A[:, id] /= link_sum
        A[:, id] *= -d
        A[id, id] = 1
    B = (1-d) * np.ones((matrix_size, 1))
    ranks = np.linalg.solve(A, B)
    return {idx: r[0] for idx, r in enumerate(ranks)}

def summarize(text, sent_num=3):
    sentences = text2sentences(text)
    nouns = get_nouns(sentences)
    
    sent_graph = build_sent_graph(nouns)
    sent_rank_idx = get_ranks(sent_graph)
    sorted_sent_rank_idx = sorted(sent_rank_idx, key=lambda k: sent_rank_idx[k], reverse=True)

    summary = []
    index = []
    for idx in sorted_sent_rank_idx[:sent_num]:
        index.append(idx)

    index.sort()
    for idx in index:
        summary.append(sentences[idx])
    
    return ' '.join(summary)

def clean_text(text):
    # 1. 'YYYY.MM.DD' 형태의 날짜 패턴 제거
    text = re.sub(r'\d{4}\.\d{1,2}\.\d{1,2}', '', text)
    
    # 2. '재판매 및 DB 금지' 텍스트 제거
    text = re.sub(r'재판매 및 DB 금지', '', text)
    
    # 3. '@'가 포함된 텍스트 제거
    text = re.sub(r'\S*@\S*\s?', '', text)

    # 4. '~ 기자' 패턴 제거
    text = re.sub(r'\S* 기자', '', text)

    # 5. '<사진=디즈니>' 와 같은 패턴 제거
    text = re.sub(r'<.*?>', '', text)
    
    # 6. '[이데일리 김윤지 기자]' 와 같이 '[ ]' 형태 제거 및 안에 텍스트 모두 제거
    text = re.sub(r'\[.*?\]', '', text)
    
    # 7. '<AFP연합뉴스>'와 같은 패턴 제거
    text = re.sub(r'<.*?\>', '', text)

    # 7. '<AFP연합뉴스>'와 같은 패턴 제거
    text = re.sub(r'【.*?\】', '', text)

    # 1. 특수기호 삭제
    text = re.sub(r'[ⓒ▲◆▶■\[\]=+\#/\?^@*※~!]', '', text)

    # 8. 여러 개의 탭(\t)이나 줄바꿈(\n)을 하나의 띄어쓰기로 대체
    text = re.sub(r'[\t\n]+', ' ', text)
    
    return text.strip()

# 엑셀 파일 읽기
file_path = './data/article_df_240812.xlsx'
df = pd.read_excel(file_path)

# 상위 20개의 데이터 선택
df_top20 = df.head(30)

# 요약된 문장을 저장할 새로운 열 생성
df_top20['cleaned_main'] = df_top20['main'].apply(clean_text)
#최대 100자(DB기준 VAR(225))
df_top20['summary'] = df_top20['cleaned_main'].apply(lambda x: summarize(x, sent_num=3))

# 요약된 데이터를 저장할 엑셀 파일 경로
output_file_path = './data/article_df_240821_summary_top30.xlsx'

# 엑셀 파일로 저장
df_top20.to_excel(output_file_path, index=False)

print(f"상위 20개의 요약된 데이터를 {output_file_path}에 저장했습니다.")
