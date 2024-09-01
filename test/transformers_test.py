from transformers import pipeline

# 요약 파이프라인 설정
summarizer = pipeline("summarization")

# 예시 텍스트
text = """
여기에 요약하고자 하는 긴 텍스트를 넣습니다. 텍스트가 길면 요약의 품질이 더 좋아집니다.
"""

# 요약 생성
summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
print(summary[0]['summary_text'])
