import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os
import ssl
from tqdm.asyncio import tqdm as tqdm_asyncio

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from ai_crud import upsert_newspapers
from ai_model import SQLMODEL
from util.hash_utils import get_sha256_hash
from util.datetime_util import convert_NAVER_date_to_datetime
import news_summary

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

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


async def fetch_html(session, url):
    """Helper function to fetch HTML from a URL asynchronously."""
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Failed to fetch {url}: {e}")
        return None


async def ex_tag(session, sid, page):
    """Extracts article links from a given sid and page asynchronously."""
    url = f"https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1={sid}&date=%2000:00:00&page={page}"
    html = await fetch_html(session, url)
    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    return [
        a["href"]
        for a in soup.find_all("a", href=True)
        if a["href"].startswith("https://n.news.naver.com/mnews/article/")
        and "/comment/" not in a["href"]
    ]


async def re_tag(session, sid):
    """Collects unique article links for a specific sid asynchronously."""
    tasks = [ex_tag(session, sid, i + 1) for i in range(100)]
    results = await tqdm_asyncio.gather(*tasks, desc=f"Collecting links for SID {sid}")

    unique_links = set(link for sublist in results for link in sublist)
    return list(unique_links)


async def art_crawl(session, url):
    """Crawls article details given a URL asynchronously."""
    html = await fetch_html(session, url)
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


async def main():
    sids = [100, 101, 102, 103, 104, 105]
    all_hrefs = {}

    async with aiohttp.ClientSession(
        headers=HEADERS, connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as session:
        # Step 1: Collect links asynchronously
        for sid in sids:
            all_hrefs[sid] = await re_tag(session, sid)

        # Step 2: Crawl article data in parallel asynchronously
        tasks = [
            art_crawl(session, url) for sid, urls in all_hrefs.items() for url in urls
        ]
        results = await tqdm_asyncio.gather(*tasks, desc="Crawling articles")

        artdic_lst = []
        for sid, urls in all_hrefs.items():
            for result in results:
                if result and result["link"] in urls:
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
            summary=news_summary.get_summary(row["main"]),
            link=row["link"],
            link_hash=get_sha256_hash(row["link"]),
            image=row["image"],
            source=row["source"],
            published_at=convert_NAVER_date_to_datetime(row["published_at"]),
        )
        for _, row in art_df.iterrows()
    ]

    upsert_newspapers(newspapers=newspapers)


def run():
    print("[크롤링-NAVER]시작")
    asyncio.run(main())
    print("[크롤링-NAVER]종료")
