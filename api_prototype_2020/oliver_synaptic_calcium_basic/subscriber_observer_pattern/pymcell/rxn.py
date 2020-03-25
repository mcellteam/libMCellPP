from .model_part import *
from .model_rxn_ifce import *

class Rxn(ModelPart):

    def __init__(self, name, fwd_rate, reactants, products, bkwd_rate=None):
        ModelPart.__init__(self)

        self.name = name
        self._fwd_rate = fwd_rate
        self.reactants = reactants
        self.products = products
        self.bkwd_rate = bkwd_rate

    def __del__(self):
        while len(self.subscribed_models) != 0:
            self.subscribed_models.pop().remove_rxn(self)

    @property
    def fwd_rate(self):
        return self._fwd_rate

    @fwd_rate.setter
    def fwd_rate(self, value):
        self._fwd_rate = value

        # Notify
        for m in self.subscribed_models:
            m.notify_fwd_rate_changed(self, value)
