import requests
from bs4 import BeautifulSoup
import sys
import os
from typing import Optional

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import ai_exception


def get_news_info_from_NAVER(link: str) -> tuple[str, str, Optional[str], str, str]:
    """
    Raises:
        ai_exception.InvalidURLError: The URL Type is not matched
        ai_exception.URLNotFoundError: The provided URL was not found
        ai_exception.URLNotCrawlableError: URL Is Not Crawlable

    Returns:
        tuple[str, str, Optional[str], str, str]: title, body, image, source, published_at
    """
    link = "https://" + link

    try:
        response = requests.get(link, timeout=3)
    except requests.exceptions.InvalidURL:
        raise ai_exception.InvalidURLError
    except (requests.exceptions.Timeout, requests.exceptions.HTTPError):
        raise ai_exception.URLNotFoundError
    except Exception as e:
        raise e

    soup = BeautifulSoup(response.text, "html.parser")

    # 1. 헤드라인 추출
    title_meta = soup.find("meta", property="og:title")
    image_meta = soup.find("meta", property="og:image")
    body_tag = soup.find("article", id="dic_area")
    source_meta = soup.find("meta", attrs={"name": "twitter:creator"}) or soup.find(
        "meta", property="og:article:author"
    )
    published_at_tag = soup.find(
        "span", class_="media_end_head_info_datestamp_time _ARTICLE_DATE_TIME"
    )

    if (
        title_meta is None
        or body_tag is None
        or source_meta is None
        or published_at_tag is None
    ):
        raise ai_exception.URLNotCrawlableError

    title = title_meta["content"]
    body = body_tag.get_text(separator=" ", strip=True)
    image = image_meta["content"] if image_meta else None
    source = source_meta["content"]
    published_at = published_at_tag["data-date-time"]

    return title, body, image, source, published_at


# def test():
#     result = get_news_info_from_NAVER("n.news.naver.com/article/033/0000047648")
#     print(result)
#     result1 = get_news_info_from_NAVER("n.news.naver.com/article/009/0005359490")
#     print(result1)
#     # result2 = get_news_info_from_NAVER("n.news.naver.com")
#     # print(result2)
#     result3 = get_news_info_from_NAVER("https://n.news.naver.com/mnews/hotissue/article/003/0012763017")
#     print(result3)


# test()
