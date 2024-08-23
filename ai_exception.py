class UserNotFoundError(Exception):
    def __init__(self, message="This User ID was not found"):
        super().__init__(message)


class InvalidURLError(Exception):
    def __init__(self, message="The provided URL is invalid"):
        super().__init__(message)


class URLNotCrawlableError(Exception):
    def __init__(self, message="The page cannot be crawled"):
        super().__init__(message)
