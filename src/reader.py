from abc import ABC, abstractmethod


class Reader(ABC):

    @abstractmethod
    def get_new_data(self):
        pass
