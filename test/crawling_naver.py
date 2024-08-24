import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from ai_crud import create_newspapers
from ai_model import SQLMODEL

# Constants
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
CATEGORY_MAP = {
    100: "정치",
    101: "경제",
    102: "사회",
    103: "생활/문화",
    104: "세계",
    105: "IT/과학",
}


def fetch_html(url):
    """Helper function to fetch HTML from a URL."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None


def ex_tag(sid, page):
    """Extracts article links from a given sid and page."""
    url = f"https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1={sid}&date=%2000:00:00&page={page}"
    html = fetch_html(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    return [
        a["href"]
        for a in soup.find_all("a", href=True)
        if a["href"].startswith("https://n.news.naver.com/mnews/article/")
        and "/comment/" not in a["href"]
    ]


def re_tag(sid):
    """Collects unique article links for a specific sid."""
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(ex_tag, sid, i + 1) for i in range(100)]
        results = [f.result() for f in tqdm(futures, desc=f"Processing SID {sid}")]

    unique_links = set(link for sublist in results for link in sublist)
    return list(unique_links)


def art_crawl(url):
    """Crawls article details given a URL."""
    html = fetch_html(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "lxml")
    title = soup.select_one("#title_area > span")
    date = soup.select_one(
        "#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div:nth-child(1) > span"
    )
    publisher_tag = soup.select_one(
        "#ct > div.media_end_head.go_trans > div.media_end_head_top._LAZY_LOADING_WRAP > a > img.media_end_head_top_logo_img.light_type._LAZY_LOADING._LAZY_LOADING_INIT_HIDE"
    )
    img_tag = soup.select_one("#img1")
    main = soup.select_one("#dic_area")

    return {
        "title": title.text.strip() if title else "",
        "published_at": date.text.strip() if date else "",
        "source": (
            publisher_tag["alt"]
            if publisher_tag and "alt" in publisher_tag.attrs
            else ""
        ),
        "image": (
            (
                img_tag.get("src")
                or img_tag.get("data-src")
                or img_tag.get("data-original")
                or img_tag.get("data-lazy")
                or ""
            )
            if img_tag
            else ""
        ),
        "main": main.text.strip() if main else "",
        "link": url,
    }


def main():
    sids = [100, 101, 102, 103, 104, 105]
    all_hrefs = {}

    # Step 1: Collect links
    for sid in sids:
        all_hrefs[sid] = re_tag(sid)

    # Step 2: Crawl article data in parallel
    artdic_lst = []
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(art_crawl, url): (sid, url)
            for sid, urls in all_hrefs.items()
            for url in urls
        }
        for future in tqdm(futures, desc="Crawling articles"):
            result = future.result()
            if result:
                sid, url = futures[future]
                result["section"] = sid
                artdic_lst.append(result)

    # Step 3: Convert to DataFrame
    art_df = pd.DataFrame(artdic_lst)
    art_df["category"] = art_df["section"].map(CATEGORY_MAP)

    # Step 4: Create SQLMODEL.NewsPaper objects and save to DB
    newspapers = [
        SQLMODEL.NewsPaper(
            title=row["title"],
            body=row["main"],
            summary="TEMP SUMMARY",
            link=row["link"],
            image=row["image"],
            source=row["source"],
            published_at=row["published_at"],
        )
        for _, row in art_df.iterrows()
    ]
    create_newspapers(newspapers=newspapers)


main()