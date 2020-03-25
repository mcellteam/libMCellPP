from .rxn import *

class Model(ModelRxnIfce):

    def __init__(self):
        self.rxns = set()

    ########################################
    # Reactions
    ########################################

    def add_rxn(self, rxn):
        self.rxns.add(rxn)

        # Subscribe
        rxn.add_model_to_subscribers(self)

    def remove_rxn(self, rxn):
        self.rxns.discard(rxn)

        # Unsubscribe
        rxn.remove_model_from_subscribers(self)

    def notify_fwd_rate_changed(self, rxn, fwd_rate):
        print(">>> In Model: We now have a callback for the reaction: %s notifying that the rate has been changed to: %f" % (rxn.name, fwd_rate))
