from abc import ABC, abstractmethod
from collections import UserDict


class AbstractNotebook(ABC, UserDict):
    @abstractmethod
    def add_record(self, record):
        pass

    @abstractmethod
    def edit_record(self, title, new_note):
        pass

    @abstractmethod
    def remove_record(self, title):
        pass

    @abstractmethod
    def show_all_record(self):
        pass


class AbstractMenuBook(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def print_table(self):
        pass
