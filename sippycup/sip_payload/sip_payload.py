from abc import ABC, abstractmethod


class SipPayload(ABC):
    @abstractmethod
    def payload(self, args):
        pass
