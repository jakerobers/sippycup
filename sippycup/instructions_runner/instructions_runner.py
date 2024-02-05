from abc import ABC, abstractmethod

class InstructionsRunner(ABC):
    @abstractmethod
    def r(self, args):
        pass

    @abstractmethod
    def o(self, args):
        pass

    @abstractmethod
    def i(self, args):
        pass

    @abstractmethod
    def ai(self, args):
        pass

    @abstractmethod
    def di(self, args):
        pass

