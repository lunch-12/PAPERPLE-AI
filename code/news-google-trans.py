#pip install googletrans==4.0.0-rc1
import pandas as pd
from googletrans import Translator

# Translator 객체 생성
translator = Translator()

# 엑셀 파일 읽기
file_path = 'data/yahoo_aritcle_240813.xlsx'  # 여기에 실제 파일 경로를 입력하세요.
df = pd.read_excel(file_path)

def clean_text(text):
    # "Story Continues"와 "View Comments" 제거
    text = text.replace("Story Continues", "").replace("View Comments", "")
    return text

# 'main' 열을 먼저 정리한 후, 번역하여 'translated_main'이라는 새로운 열로 저장
df['translated_main'] = df['main'].apply(lambda x: translator.translate(clean_text(x), src='en', dest='ko').text if pd.notnull(x) else x)

# 번역된 데이터를 저장할 엑셀 파일 경로
output_file_path = './data/yahoo_aritcle_translated.xlsx'

# 엑셀 파일로 저장
df.to_excel(output_file_path, index=False)

print(f"번역된 데이터를 {output_file_path}에 저장했습니다.")
