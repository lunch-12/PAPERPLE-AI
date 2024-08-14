"""
#카테고리별 네이버 기사 크롤링
- 카테고리별로 크롤링하여 제목, 날짜, 본문, 카테고리, 링크의 속성을 가진 데이터프레임 생성

### 한 카테고리와 페이지에서 뉴스 기사 링크 수집
- 한 카테고리에서 100페이지까지의 뉴스 기사 링크 수집
- 정치, 경제, 사회, 생활/문화, 세계, IT/과학 등의 6가지 카테고리(100~105)
"""

import requests
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm

def ex_tag(sid, page):
    ### 뉴스 분야(sid)와 페이지(page)를 입력하면 그에 대한 링크들을 리스트로 추출하는 함수 ###

    ## 1.
    url = f"https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1={sid}&date=%2000:00:00&page={page}"
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"\
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "\
    "Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")
    a_tag = soup.find_all("a")
    #print(a_tag)
    ## 2.
    tag_lst = []
    for a in a_tag:
        if "href" in a.attrs:  # href가 있는것만 고르는 것
            href = a["href"]
            # https://n.news.naver.com/mnews/article/ 형식의 URL만 추출하는 조건
            if href.startswith("https://n.news.naver.com/mnews/article/") and "/comment/" not in href:
                tag_lst.append(href)


    return tag_lst

def re_tag(sid):
    ### 특정 분야의 100페이지까지의 뉴스의 링크를 수집하여 중복 제거한 리스트로 변환하는 함수 ###
    re_lst = []
    for i in tqdm(range(100)):
        lst = ex_tag(sid, i+1)
        re_lst.extend(lst)

    # 중복 제거
    re_set = set(re_lst)
    re_lst = list(re_set)

    return re_lst

all_hrefs = {}
sids = [i for i in range(100,106)]  # 분야 리스트

# 각 분야별로 링크 수집해서 딕셔너리에 저장
for sid in sids:
    sid_data = re_tag(sid)
    all_hrefs[sid] = sid_data

"""## 기사 제목, 게시일, 본문, 카테고리, 링크 수집
- 각각의 뉴스 기사 링크에 접속해서 들어간 화면에서 기사제목, 게시일, 수정시간, 본문, 이미지, 발행보도사를 크롤링하여 딕셔너리를 출력
- 비고) 생성시간(네이버뉴스에서는 게시일과 동일처리)
"""

def art_crawl(all_hrefs, sid, index):
    """
    sid와 링크 인덱스를 넣으면 기사제목, 게시일, 본문을 크롤링하여 딕셔너리를 출력하는 함수

    Args:
        all_hrefs(dict): 각 분야별로 100페이지까지 링크를 수집한 딕셔너리 (key: 분야(sid), value: 링크)
        sid(int): 분야 [100: 정치, 101: 경제, 102: 사회, 103: 생활/문화, 104: 세계, 105: IT/과학]
        index(int): 링크의 인덱스

    Returns:
        dict: 기사제목, 게시일, 수정시간, 본문, 발행보도사가 크롤링된 딕셔너리

    """
    art_dic = {}

    ## 1.
    title_selector = "#title_area > span"
    date_selector = "#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans"\
    "> div.media_end_head_info_datestamp > div:nth-child(1) > span"
    updated_at_selector = "#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans"\
    "> div.media_end_head_info_datestamp > div:nth-child(2) > span"
    main_selector = "#dic_area"
    publisher_selector = "#ct > div.media_end_head.go_trans > div.media_end_head_top._LAZY_LOADING_WRAP"\
    " > a > img.media_end_head_top_logo_img.light_type._LAZY_LOADING._LAZY_LOADING_INIT_HIDE"
    img_selector = "#img1"


    url = all_hrefs[sid][index]
    html = requests.get(url, headers = {"User-Agent": "Mozilla/5.0 "\
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"\
    "Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")

    ## 2.
    # 제목 수집
    title = soup.select(title_selector)
    title_lst = [t.text for t in title]
    title_str = "".join(title_lst)

    # 날짜 수집
    date = soup.select(date_selector)
    date_lst = [d.text for d in date]
    date_str = "".join(date_lst)

    # # 수정 시간 수집
    # updated_date = soup.select_one(updated_at_selector)
    # updated_str = updated_date.text if updated_date else ""

    #발행보도사 수집
    publisher_tag = soup.select_one(publisher_selector)
    publisher = publisher_tag['alt'] if publisher_tag and 'alt' in publisher_tag.attrs else ""

    #이미지 수집
    img_tag = soup.select_one(img_selector)
    #img_src = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ""
    img_src = (
        img_tag.get('src') or
        img_tag.get('data-src') or
        img_tag.get('data-original') or
        img_tag.get('data-lazy') or
        ""
    ) if img_tag else ""

    # 본문 수집
    main = soup.select(main_selector)
    main_lst = []
    for m in main:
        m_text = m.text
        m_text = m_text.strip()
        main_lst.append(m_text)
    main_str = "".join(main_lst)

    ## 3.
    art_dic["title"] = title_str
    art_dic["published_at"] = date_str
    # art_dic["updated_at"] = updated_str
    art_dic["source"] = publisher
    art_dic["image"] = img_src
    art_dic["main"] = main_str  # 본문 # 이를 사용하여 요약본 추가예정

    return art_dic

# 모든 섹션의 데이터 수집 (section, url 포함)
section_lst = [s for s in range(100, 106)]
artdic_lst = []

for section in tqdm(section_lst):
    for i in tqdm(range(len(all_hrefs[section]))):
        art_dic = art_crawl(all_hrefs, section, i)
        art_dic["section"] = section
        art_dic["link"] = all_hrefs[section][i]
        artdic_lst.append(art_dic)

import pandas as pd
art_df = pd.DataFrame(artdic_lst)

# 카테고리 ID와 이름의 매핑
category_map = {
    100: "정치",
    101: "경제",
    102: "사회",
    103: "생활/문화",
    104: "세계",
    105: "IT/과학"
}
# 이미 존재하는 art_df 데이터프레임에서 category 열을 매핑
art_df['category'] = art_df['section'].map(category_map)

# 결과 확인
art_df.head()

# pandas의 to_excel 메서드를 사용하여 엑셀 파일로 저장합니다.
# art_df.to_excel("article_df_240812.xlsx", index=False)

art_df.groupby("section").size() #100페이지를 크롤링하고 중복 기사를 제거한 결과