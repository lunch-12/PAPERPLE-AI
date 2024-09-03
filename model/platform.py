import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from crawling import crawling_news
from typing import Callable, Optional


class Platform:
    __supported_domains_and_crawling_methods = {
        "n.news.naver.com": crawling_news.get_news_info_from_NAVER,
        "news.naver.com": crawling_news.get_news_info_from_NAVER,
        "v.daum.net": crawling_news.get_news_info_from_DAUM,
        "news.nate.com": crawling_news.get_news_info_from_NATE,
        "m.news.nate.com": crawling_news.get_news_info_from_NATE_MOBILE,
    }

    __supported_domains_and_date_format = {
        "n.news.naver.com": "%Y-%m-%d %H:%M:%S",
        "news.naver.com": "%Y-%m-%d %H:%M:%S",
        "v.daum.net": "%Y%m%d%H%M%S",
        "m.news.nate.com": "%Y.%m.%d %H:%M",
        "news.nate.com": "%Y-%m-%d %H:%M",
    }

    @classmethod
    def isSupported(cls, domain: str) -> bool:
        print("[START]isSupported, domain:", domain)
        return domain in cls._Platform__supported_domains_and_crawling_methods

    @classmethod
    def get_crawling_method(
        cls, domain: str
    ) -> Callable[[str], tuple[str, str, Optional[str], str, str]]:
        """
        ex) Platform.get_crawling_method(domain=domain)(link)
        Returns:
            function: 지정된 도메인에서 콘텐츠를 크롤링할 수 있는 함수, 인자로 link를 받음.\n
            function: (link:str) -> tuple[str, str, Optional[str], str, str]: (title, body, image, source, published_at)

        Raises:
            Exception: 도메인이 지원되지 않는 경우 KeyError 발생할 수 있음.
        """
        print("[START]get_crawling_method, domain:", domain)
        return cls._Platform__supported_domains_and_crawling_methods[domain]

    @classmethod
    def get_date_format(cls, domain: str) -> str:
        print("[START]get_date_format, domain:", domain)
        return cls._Platform__supported_domains_and_date_format[domain]


# def test():
#     print(Platform.isSupported("n.news.naver.com"))
#     print(Platform.isSupported("n.news.naver"))
#     print(
#         Platform.get_crawling_method("n.news.naver.com")(
#             "n.news.naver.com/mnews/article/277/0005467022"
#         )
#     )


# test(
