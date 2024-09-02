class UserNotFoundError(Exception):
    def __init__(self, message="This User ID was not found"):
        super().__init__(message)


class InvalidURLError(Exception):
    def __init__(self, message="The URL Type is not matched"):
        super().__init__(message)


class URLNotFoundError(Exception):
    def __init__(self, message="The provided URL was not found"):
        super().__init__(message)


class URLNotCrawlableError(Exception):
    def __init__(self, message="The page cannot be crawled"):
        super().__init__(message)


class NotSupportedException(Exception):
    def __init__(self, message="This platform does not support the service."):
        super().__init__(message)
