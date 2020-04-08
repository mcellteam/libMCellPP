#!/usr/bin/env python3

# pip3 install python-varname
from varname import varname
import copy
 
 # not executable
 
# -------------------------  definition of molecule types and reactions --------------
                
# -------------------------  CaM --------------    

# it is not possible to define a standalone component


# molecule type
CaM = MoleculeType(
    'Cam(N~0~1~2,C~0~1~2)',
    diff_const = 10.0,
)

# -------------------------  CaMKII --------------


CaMKII = MoleculeType(
    'CaMKII(d,r,l,Y286~0~P,S306~0~P,cam)',
    diff_const =10.0,
)
    
print("Molecule type declaration:")
print(CaM)
print("")
    
print("Molecule type declaration:")
print(CaMKII)
print("")

mol_type_inst = MoleculeInstance('CaMKII(d,r,l,Y286~0,S306~0,cam')

print("Molecule type instance:")
print(mol_type_inst)
print("")

# this is already an instance of a complex
# serves as a pattern when used in a reaction
cplx = ComplexInstance('CaMKII(l!1,r,Y286~0,cam!+).CaMKII(l,r!1,cam!+)')

print("Complex instance:")
print(cplx)
print("")


V = 0.125*1e-15 # um^3 -> liters
NA = 6.022e23/1e6
k_onCaMKII = 50/(NA*V) #1/uM 1/s 
k_offCaMKII = 60 #1/s 
    
# CaMKII(l,r,Y286~0,cam!+) + CaMKII(l,r,cam!+) <-> CaMKII(l!1,r,Y286~0,cam!+).CaMKII(l,r!1,cam!+) k_onCaMKII, k_offCaMKII    
rxn = RxnRule(
    name = "sixth rxn",
    fwd_rate = k_onCaMKII,
    rev_rate = k_offCaMKII, # I found more often 'reverse reaction' to be used than 'backward reaction', but please comment on this if bkwd_rate makes more sense
    # note: components are in different order than in molecule type definition, this is apparently allowed
    
    # component patter is used with the meaning that when no state is specified, any state is fine
    reactants=[
        ComplexPattern('CaMKII(l,r,Y286~0,cam!+)'),
        ComplexPattern('CaMKII(l,r,Y286~0,cam!+)')
    ],
    products=[
        ComplexPattern('CaMKII(l!1,r,Y286~0,cam!+).CaMKII(l,r!1,cam!+)')
    ]
)


print("Reaction rule:")
print(rxn)
print("")


