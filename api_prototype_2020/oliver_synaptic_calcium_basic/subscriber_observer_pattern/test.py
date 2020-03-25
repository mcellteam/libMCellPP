from pymcell import *

rxn = Rxn(
    name="my_rxn",
    fwd_rate=1.0,
    reactants=["A","B"],
    products=["C"]
)

print("Made reaction: %s with rate: %f" % (rxn.name, rxn.fwd_rate))

m = Model()
m.add_rxn(rxn)

print("Added rxn to model")

print("Changing the reaction rate by calling: rxn.fwd_rate = 10.0")

rxn.fwd_rate = 10.0

print("Changed fwd rate of reaction: %s to: %f" % (rxn.name, rxn.fwd_rate))
