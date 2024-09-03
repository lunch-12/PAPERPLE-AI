import ai_model
import ai_crud
import ai_exception
from util.hash_utils import get_sha256_hash
from util.url_util import get_domain_and_path
from util.datetime_util import convert_str_to_datetime
from model import platform
from news_summary import get_summary


def crawl_and_write_newspaper(url: str) -> ai_model.APIMODEL.NewsPaper:
    """
    1. 해당 URL의 뉴스를 크롤링하고, 요약합니다
    2. 요약한 정보를 RDS에 저장합니다
    3. 뉴스 정보를 리턴합니다

    Raises:
        ai_exception.InvalidURLError: The URL Type is not matched
        ai_exception.URLNotFoundError: The provided URL was not found
        ai_exception.URLNotCrawlableError: URL Is Not Crawlable

    Args:
        url (str): 크롤링 하고자 하는 뉴스의 URL
    """
    print("[START]crawl_and_write_newspaper, url:", url)
    # URL 도메인 추출
    try:
        domain, path = get_domain_and_path(url)
        link = domain + path
    except Exception:
        raise ai_exception.InvalidURLError

    # 지원하는 도메인인지 확인
    if not platform.Platform.isSupported(domain=domain):
        raise ai_exception.NotSupportedException

    # RDS에 존재하는지 확인
    link_hash = get_sha256_hash(link)
    try:
        newspaper = ai_crud.read_newspaper(link_hash=link_hash)
        return ai_model.APIMODEL.NewsPaper(
            title=newspaper.title,
            summary=newspaper.summary,
            link=newspaper.link,
            image=newspaper.image,
            source=newspaper.source,
            published_at=newspaper.published_at.isoformat(),
        )

    except Exception:
        # news 크롤링
        try:
            title, body, image, source, published_at = (
                platform.Platform.get_crawling_method(domain=domain)(link)
            )

            summary = get_summary(body)
            published_at = convert_str_to_datetime(
                date_str=published_at,
                date_format=platform.Platform.get_date_format(domain=domain),
            )

            # DB 저장
            sql_newspaper = ai_model.SQLMODEL.NewsPaper(
                title=title,
                body=body,
                summary=summary,
                link=link,
                link_hash=link_hash,
                image=image,
                source=source,
                published_at=published_at,
            )
            ai_crud.upsert_newspapers([sql_newspaper])

            return ai_model.APIMODEL.NewsPaper(
                title=title,
                summary=summary,
                link=link,
                image=image,
                source=source,
                published_at=published_at.isoformat(),
            )

        except Exception as e:
            raise e


# def get_newspapers_for_user(user_id: int) -> ai_model.APIMODEL.Newspapers:
#     # 1. User ID로 페이지 리스트 받아오기
#     page = 0
#     page_count = 10
#     newspapers = []

#     return ai_model.APIMODEL.Newspapers(
#         page=page, page_count=page_count, newspapers=newspapers
#     )
