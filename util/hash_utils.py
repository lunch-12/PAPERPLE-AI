import hashlib


def get_sha256_hash(string: str) -> str:
    string_encoded = string.encode()
    return hashlib.sha256(string_encoded).hexdigest()


# def test():
#     print(get_sha256_hash("n.news.naver.com/article/033/0000047648")) 
#     a2de8839d7f32bb07bd9505612796d7abda66a8bc2a32e0a7ac046f20f279fb2
#     print(get_sha256_hash("v.daum.net/v/20240902082702793"))
#     print(get_sha256_hash("mk.co.kr/news/it/10952368"))


# test()
