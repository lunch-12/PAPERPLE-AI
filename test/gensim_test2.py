# -*- coding: utf-8 -*- 
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np

# 자연어처리
## 꼬꼬마분석기
kkma = Kkma() 

## text를 입력받아 Kkma.sentences()를 이용해 문장단위로 나눈 뒤 sentences로 리턴
def text2sentences(text):  
    sentences = kkma.sentences(text)  #text일 때 문장별로 리스트 만듦
    for idx in range(0, len(sentences)):  #길이에 따라 문장 합침(위와 동일)
        if len(sentences[idx]) <= 10:
            sentences[idx-1] += (' ' + sentences[idx])
            sentences[idx] = ''
    return sentences

## 기사본문 가져오기(리스트형태로)
text = """
중앙위 의결…18일 全大서 확정경선불복 → 공천불복 제재 확대더불어민주당은 12일 당 중앙위원회에서 ‘기본사회’와 ‘당원 중심주의’를 담은 강령 개정안을 채택한다. 기본사회는 이재명 전 대표의 대표적인 복지 정책이고, 당원 중심주의는 이 전 대표가 추구하는 새로운 정당의 모습이다. ‘경선 불복에 대한 제재’를 ‘공천 불복에 대한 제재’로 수정하는 내용 등을 담은 당헌 개정안도 중앙위에 오른다.민주당은 이날 중앙위 온라인 투표를 통해 ‘기본사회’ ‘당원 중심주의’를 명시한 강령 개정안을 의결한다. 이 개정안은 민주당 8·18 전국당원대회에서 최종 확정될 것으로 관측된다. 강령 개정안 전문에는 모든 사람이 공정하고 동등한 조건에서 역량을 발휘하는 ‘정의로운 나라’, 사회경제적 양극화·불평등을 극복하고 기본적인 삶을 보장하는 ‘기본사회’, 계층·세대·성별·지역 갈등을 해소하고 모든 국민의 조화로운 삶을 지향하는 ‘통합의 국가’ 등이 명시됐다. 더 강한 민주주의와 당원 중심 대중 정당을 목표로 당원 중심 정당 강화 방향을 구체화해야 한다는 내용도 담겼다. 강령 개정안이 전당대회를 거쳐 최종 확정되면 민주당 내 이 전 대표 체제가 한층 강화될 것으로 보인다.중앙위는 당헌 84조의 ‘선거부정 및 경선 불복에 대한 제재’를 ‘공천 불복에 대한 제재’로 수정하는 당헌 개정안도 의결한다. 민주당은 지난 6월 당헌 100조의 당내 경선 시 감산 대상을 기존 ‘경선 불복 경력자’에서 ‘공천 불복 경력자’로 개정했다. 다만 당내 일각에서는 후보자가 중앙당의 전략공천이나 컷오프(공천 배제) 결정에 항의할 수 있는 길을 차단하는 게 아니냐는 지적을 제기하고 있다."""

sentences = text2sentences(text)
## print(sentences)
twitter = Twitter()

## 불용어제거
stopwords = ['머니투데이' , "연합뉴스", "데일리", "동아일보", "중앙일보", "조선일보", "기자","아", "휴", "아이구", "아이쿠", "아이고", "어", "나", "우리", "저희", "따라", "의해", "을", "를", "에", "의", "가",]

def get_nouns(sentences):
    nouns = []
    for sentence in sentences:
        if sentence != '':
            nouns.append(' '.join([noun for noun in twitter.nouns(str(sentence))
                                  if noun not in stopwords and len(noun) > 1]))
    return nouns

nouns = get_nouns(sentences)
#print(nouns)

# TF-IDF 모델 생성 및 그래프 생성
## 앞에서 명사로 이루어진 문장리스트를 입력받아 
## sklearn의 TfidVectorizer.fit_transform을 이용하면 TF-IDF matrix
tfidf = TfidfVectorizer()
cnt_vec = CountVectorizer()
graph_sentence = []

def build_sent_graph(sentence):
    tfidf_mat = tfidf.fit_transform(sentence).toarray()
    graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
    return graph_sentence

sent_graph = build_sent_graph(nouns)

## 단어 단위에 대한 word graph를 만들고, 
## {idx : word} 형태의 딕셔너리를 만들기 위해 sklearn의 CountVectorizer.fit_transform을 사용해준다. 
## 단어에 대해서도 word graph를 만드는 이유는 가장 순위가 높은 문장들 말고도 가장 순위가 높은 keyword를 찾아보려고 하기 위함
def build_words_graph(sentence):
    cnt_vec_mat = normalize(cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
    vocab = cnt_vec.vocabulary_
    return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}
    
words_graph, idx2word = build_words_graph(nouns)

#print(idx2word)

# TextRank 구현하기
## 구한 가중치 그래프를 이용하여 TextRank 알고리즘(수식)에 넣어 점수를 매기고
## 순위가 높은 순으로 정렬한 뒤, 요약할 문장의 개수만큼 출력

def get_ranks(graph, d=0.85): # d = damping factor
    A = graph
    matrix_size = A.shape[0]
    for id in range(matrix_size):
        A[id, id] = 0 # diagonal 부분을 0으로
        link_sum = np.sum(A[:,id]) # A[:, id] = A[:][id]
        if link_sum != 0:
            A[:, id] /= link_sum
        A[:, id] *= -d
        A[id, id] = 1

    B = (1-d) * np.ones((matrix_size, 1))
    ranks = np.linalg.solve(A, B) # 연립방정식 Ax = b
    return {idx: r[0] for idx, r in enumerate(ranks)}
sent_rank_idx = get_ranks(sent_graph)  #sent_graph : sentence 가중치 그래프
sorted_sent_rank_idx = sorted(sent_rank_idx, key=lambda k: sent_rank_idx[k], reverse=True)

word_rank_idx = get_ranks(words_graph)
sorted_word_rank_idx = sorted(word_rank_idx, key=lambda k: word_rank_idx[k], reverse=True)

# 요약하기 실행
## 기사 본문에 대해서 각 문장과 단어마다의 점수를 매기고, 
## 인덱스 값을 정렬해놨으니 이제 TextRank값이 높은 문장들을 출력
def summarize(sent_num=5):
    summary = []
    index=[]
    for idx in sorted_sent_rank_idx[:sent_num]:
        index.append(idx)

    index.sort()
#     print(index)
    
    for idx in index:
        summary.append(sentences[idx])

    for text in summary :
        print(text)

summarize(3)