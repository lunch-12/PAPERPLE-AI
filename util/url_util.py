from urllib.parse import urlparse
from typing import Optional
import re


def get_domain_and_path(url: Optional[str]) -> tuple[str, str]:
    """
    get Domain from url\n
    ...\n
    try:
        domain, path = get_domain_and_path(url)
    ...

    ### Raises:
        ValueError: None이거나 올바르지 않는 URL 형식
    """
    if url is None or len(url) == 0:
        raise ValueError

    parsed_url = urlparse(url.lower())
    netloc = parsed_url.netloc

    path = parsed_url.path

    if len(netloc) < 4:
        if path is not None:
            netloc = path.split("/")[0]
            path = "/" + "/".join(path.split("/")[1:])
        else:
            raise ValueError

    if len(netloc) > 6 and netloc[:4] == "www.":
        netloc = netloc[4:]

    if re.search("[^a-z0-9.-]", netloc):
        raise ValueError

    return netloc, path


# def test():
#     urls = [
#         "https://n.news.naver.com/article/033/0000047648?cds=news_media_pc&type=editn",
#         "n.news.naver.com/article/033/0000047648?cds=news_media_pc&type=editn",
#         "https://v.daum.net/v/20240902082702793",
#         "https://www.mk.co.kr/news/it/10952368",
#         "https://www.m''''''k.co.kr/news/it/10952368",
#         "asdfsadfdf",
#         None,
#         "example-com/",
#         "example.com",
#         "example-com-",
#         "-example-com",
#         "example-com",
#         "examp''le123",
#         "123example",
#         "ex-ample-com",
#         "example",
#         "ex-_-ample",
#         "",
#     ]

#     for url in urls:
#         try:
#             domain, path = get_domain_and_path(url)
#             print(domain, path)
#             print(domain + path)
#             print(type(domain + path))
#         except Exception:
#             print("ValueError")


# test()
