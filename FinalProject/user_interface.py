from abc import ABC, abstractmethod

class UserInterface(ABC):

    @abstractmethod
    def show_all(self):
        pass
