from pymcell import *

# A + B -> C
rxn = Rxn("my rxn", 1.0, ["A"], ["B", "C"])

# Make a model
model = Model()

# Add rxn
model.add_rxn(rxn)

# Change the rxn rate
rxn.fwd_rate = 3.0
