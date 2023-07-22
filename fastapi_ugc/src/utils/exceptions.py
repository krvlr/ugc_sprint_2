class BookmarksException(Exception):
    def __init__(self, error_message: str):
        self.error_message = f"Ошибка работы с закладками. {error_message}"
