import logging


class RequestUserFilter(logging.Filter):
    def filter(self, record):
        record.username = 'Anonymous'  # 기본값을 'Anonymous'로 설정
        return True
