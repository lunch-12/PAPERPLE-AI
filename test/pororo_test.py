# 문장 요약
# pip install pororo
# git clone https://github.com/kakaobrain/pororo.git
# cd pororo
# pip install -e 

from pororo import Pororo

summ = Pororo(task="summarization", model="bullet", lang="ko")
summ("20년 4월 8일 자로 아카이브에 올라온 뜨끈뜨끈한 논문을 찾았다. 카카오 브레인에서 한국어 자연어 처리를 위한 새로운 데이터셋을 공개했다는 내용이다. 자연어 추론(NLI)와 텍스트의 의미적 유사성(STS)는 자연어 이해(NLU)에서 핵심 과제. 영어나 다른 언어들은 데이터셋이 몇 개 있는데, 한국어로 된 NLI나 STS 공개 데이터셋이 없다. 이에 동기를 얻어 새로운 한국어 NLI와 STS 데이터 셋을 공개한다. 이전 의 접근 방식에 따라 기존의 영어 훈련 세트를 기계 번역(machine-translate)하고 develop set과 test set을 수동으로 한국어로 번역한다. 한국어 NLU에 대한 연구가 더 활성화되길 바라며, KorNLI와 KorSTS에 baseline을 설정하며, Github에 공개한다. NLI와 STS는 자연어 이해의 중심 과제들로 많이 이야기가 된다. 이에 따라 몇몇 벤치마크 데이터셋은 영어로 된 NLI와 STS를 공개했었다. 그러나 한국어 NLI와 STS 벤치마크  데이터셋은 존재하지 않았다. 대부분의 자연어 처리 연구가 사람들이 많이 쓰는 언어들을 바탕으로 연구  가 되기 때문. 유명한 한국어 NLU 데이터 셋이 전형적으로 QA나 감정 분석은 포함은 되어있는데 NLI나 STS는 아니다. 한국어로 된 공개 NLI나 STS 벤치마크 데이터셋이 없어서 이런 핵심과제에 적합한 한국어 NLU 모델 구축에 대한 관심이 부족했다고 생각한다. 이에 동기를 얻어 KorNLI와 KorSTS를 만들었다.")