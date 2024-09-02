# -*- coding: utf-8 -*- 
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
import nltk
def summarize_text(text, sentences_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences_count)
    summary = [str(sentence) for sentence in summary]
    return ' '.join(summary)

text='''정봉주 "이재명 이름 팔아 호가호위·실세 놀이 해""이재명팔이 방치하면 통합·탄핵·정권 탈환 어려워"'명팔이'가 누구인지 구체적인 인사는 언급안해



[서울=뉴시스] 권창회 기자 = 정봉주 더불어민주당 최고위원 후보가 12일 오전 서울 여의도 국회 소통관에서 기자회견을 열고 '이재명팔이' 세력에 대한 문제의식과 대응 계획을 밝히고 있다. 2024.08.12. kch0523@newsis.com[서울=뉴시스]신재현 김경록 기자 = 정봉주 더불어민주당 최고위원 후보가 12일 "당의 단합을 위해 '이재명 팔이'하며 실세 놀이하는 무리들을 뿌리 뽑겠다"며 "당 내부 암덩어리인 '명팔이'들을 잘라내야 한다"고 밝혔다. 정 후보는 이날 국회 소통관 기자회견을 통해 "이재명 전 대표를 팔아 권력 실세 놀이를 하고 있는 '이재명 팔이' 무리들"이라며 "지금처럼 '이재명팔이' 무리들을 방치한다면 통합도, 탄핵도, 정권 탈환도 어렵다"고 말했다.정 후보는 "이들은 이재명을 위한다며 끊임없이 내부를 갈라 치고 경쟁 상대를 적으로 규정하고 당을 분열시켜왔다"며 "이재명 이름 팔아 호가호위 정치, 실세놀이를 하고 있다"고 꼬집었다. 그는 "저는 당원대회 기간 내내 끊임없이 통합을 강조했고 맏형으로서 그 역할을 하겠다고 약속했다"며 "승리를 위해 하나가 되어야 하나 그러기 위해선 통합을 저해하는 당 내부 암덩어리인 명팔이들을 잘라내야 한다"고 강조했다. 정 후보는 "벌판에 홀로 선 이재명의 유일한 계파는 당원이었고 국민이었다. 그 정치를 우리 모두가 지켜야 한다"며 "그 최우선 과제가 이재명팔이 무리들 척결"이라고 말했다. 



[서울=뉴시스] 권창회 기자 = 정봉주 더불어민주당 최고위원 후보가 12일 오전 서울 여의도 국회 소통관에서 기자회견을 열고 '이재명팔이' 세력에 대한 문제의식과 대응 계획을 밝히고 있다. 2024.08.12. kch0523@newsis.com이번 기자회견은 최근 정 후보가 자신을 둘러싼 이재명 당대표 후보 지지자들의 비판 여론 등을 의식해 진행한 것으로 보인다. 정 후보는 최고위원 후보들 가운데 선두를 달리고 있었으나 이재명 후보가 김민석 최고위원 후보를 공개적으로 지지하면서 2위로 밀려났다. 박원석 전 정의당 의원 등은 라디오에 나와 정 후보가 이재명 후보 선거 개입에 분노했다고 폭로하면서 이 후보 지지자들의 항의에 부딪힌 정 후보는 최고위원 2위 자리를 유지할 수 있을지 여부도 불투명하다. 정 후보는 기자회견을 마친 뒤 취재진과 만나 '이재명 팔이'를 하는 구체적인 인물들은 언급하지 않았다. 그는 "누구나 알 만한 사람들"이라며 "당원대회가 끝나면 본격적으로 그들의 실체가 드러날 것이고 본격적인 당 혁신이 시작될 예정"이라고 말했다. 그러면서도 지금 전당대회를 뛰고 있는 최고위원 후보들 가운데에는 이재명 후보를 이용하는 무리가 존재하지 않는다고 강조했다. '친명(친이재명)'계 조직인 더민주전국혁신회의를 지칭하는 것이냐는 질문에는 "선거 끝난 뒤 말할 것"이라며 즉답을 피했다. 박원석 전 의원의 전언에 대해서는 "사적인 대화다 보니까 본의가 좀 과장되게 전해졌다"며 "그 이후론 박 전 의원과 통화를 안 했고 박 전 의원은 본인이 여러 말을 하고 있기 때문에 거기서 답을 찾으면 된다"고 설명했다. 이재명 후보도 개혁 대상이냐는 질문에는 "이재명 후보에 대한 믿음은 예전도, 지금도 전혀 변함이 없다"고 선을 그었다．
'''
summarize_text(text)

#!pip install sumy