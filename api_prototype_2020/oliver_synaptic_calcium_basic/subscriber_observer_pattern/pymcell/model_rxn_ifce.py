from abc import ABC,abstractmethod

class ModelRxnIfce(ABC):

    @abstractmethod
    def remove_rxn(self, rxn):
        pass

    @abstractmethod
    def notify_fwd_rate_changed(self, rxn, fwd_rate):
        pass
