#!/usr/bin/env python3

# pip3 install python-varname
from varname import varname
import copy
 
BOND_NONE = -2
BOND_PLUS = -1 

STATE_UNSET = 'state_unset'

# using BNGL naming for classes, samne as here: https://www.dropbox.com/s/rm0535pgom2zr6i/Sekar-RuleBasedPrimer-2012.pdf?dl=0
#
# also, this is just an example, there might be some things not completely thought through 
# regarding states and bonds, e.g. which are unset, which are don't care  
# 

# needed to make names shorter, definition with 5 compionents did not fit a single line

class CompType:
    def __init__(self, states=[], name=''):
        
        # name and allowed_states serve for component template
        if name: 
            self.name = name
        else:
            self.name = varname() # store the name of the created object variable (maintained with shallow copy)
            
        # states are converted to string
        self.allowed_states = []  
        for s in states:
            self.allowed_states.append(str(s))
        
    # prints out the declaration of the component in BNGL (template information)
    def __str__(self):
        res = self.name
        
        for s in self.allowed_states:
            res += '~' + s  

        return res
        
            
class CompInst:
    def __init__(self, component_type: CompType, state:str=STATE_UNSET, bond:int=BOND_NONE):
        self.component_type = component_type
        # we can check
        self.state = str(state)
        self.bond = bond
    
    def __str__(self):
        res = self.component_type.name
        
        if self.state != STATE_UNSET:
            res += '~' + self.state  

        if self.bond != BOND_NONE:
            if self.bond == BOND_PLUS:
                res += '!+'
            else:
                res += '!' + str(self.bond)
        
        return res
    
    
# same as CompInst, only a different name  
class CompPattern(CompInst):                
    pass 
        
        
class MolType:
    def __init__(self, diff_const, name = '', components=[]):
        # name, diff_const, and all_components serve for component template
        if name: 
            self.name = name
        else:
            self.name = varname() # store the name of the created object variable (maintained with shallow copy)
        self.diff_const = diff_const
        
        self.components = []
        for ct in components:
            if type(ct) != CompType:
                raise ValueError('Only objects of CompType can be passed as MolType components.')        
            self.components.append(ct)        
        self.all_components = components
       
    # prints out the declaration of the component in BNGL (template information)  
    def __str__(self):
        res = self.name + '('
        
        num_components = len(self.all_components)
        for i in range(num_components):
            res += str(self.all_components[i])
            if i != num_components-1:
                res += ',' 
        
        res += ')'
        return res        
        
        
class MolInst:
    def __init__(self, molecule_type: MolType, components=[]):
        self.molecule_type = molecule_type
        
        self.components = []
        for ci in components:
            if type(ci) != CompInst and type(ci) != CompPattern:
                raise ValueError('Only objects of CompInst or CompPattern can be passed as MolInst components.')        
            self.components.append(ci)

    # prints out speicifc instance information                
    def __str__(self):
        res = self.molecule_type.name + '('
        
        num_components = len(self.components)
        for i in range(num_components):
            res += str(self.components[i])
            if i != num_components-1:
                res += ',' 
        
        res += ')'
        return res        
           
           
class MolPattern(MolInst):
    pass


# used in reactions as reactants and products as a matching pattern       
class CplxInst:
    def __init__(self, molecule_insts):
        self.molecule_insts = []
        for mi in molecule_insts:
            if type(mi) != MolInst and type(mi) != MolPattern:
                raise ValueError('Only objects of MolInst or MolPattern can be passed as Complex constructor arguments.')        
            self.molecule_insts.append(mi)
            
            
    def __str__(self):      
        res = ''
        
        num_molecule_insts = len(self.molecule_insts)
        for i in range(num_molecule_insts):
            res += str(self.molecule_insts[i])
            if i != num_molecule_insts-1:
                res += '.' 
        return res
        
            
class CplxPattern(CplxInst):
    pass            
            
            
class RxnRule:
    def __init__(self, name, fwd_rate, rev_rate, reactants, products):
        self.name = name
        self.fwd_rate = fwd_rate
        self.rev_rate = rev_rate        
        # TODO: check types of passed objects
        self.reactants = reactants
        self.products = products
    
    def __str__(self):      
        res = ""
        res += "name: " + self.name + "\n"
        res += "fwd_rate: " + str(self.fwd_rate) + "\n"
        res += "rev_rate: " + str(self.rev_rate) + "\n"        
        res += "reactants:\n"
        for r in self.reactants:
            res += "  " + str(r) + "\n"
        res += "products:\n"
        for p in self.products:
            res += "  " + str(p) + "\n"
            
        return res
        
# -------------------------  definition of molecule types and reactions --------------
    
# -------------------------  CaM --------------    

C = CompType(   
    states = [0,1,2]
)

print("CompType declaration:")
print(C)   
print("")

N = CompType(
    states = [0,1,2]
)
ng = CompType()
camkii = CompType()

#  CaM(C~0~1~2,N~0~1~2,ng,camkii)
CaM = MolType(
    diff_const = 1e-6,
    components = [C, N, ng, camkii]
)

# -------------------------  CaMKII --------------


d = CompType() # no states  
l = CompType()
r = CompType()
Y286 = CompType(
    states = ['0','P']
)
S306 = CompType(
    states = ['0','P']
)
cam = CompType()

# CaMKII(d,r,l,Y286~0~P,S306~0~P,cam)
CaMKII = MolType(
    diff_const = 1e-6,
    components = [d, r, l, Y286, S306, cam] # we are using directly molecule types here, no need to instatiate anything
)
    
print("Molecule type declaration:")
print(CaM)
print("")
    
print("Molecule type declaration:")
print(CaMKII)
print("")

# -------------------------  example of mol inst --------------

# an instance - we already need to specify states and list all components
mol_type_inst = MolInst( CaMKII, [ CompInst(d), CompInst(r), CompInst(l), CompInst(Y286, 0), CompInst(S306, 0), CompInst(cam) ] )

print("Molecule type instance:")
print(mol_type_inst)
print("")

# -------------------------  example of cplx inst --------------

# this is already an instance of a complex
# can be used in releases (seed species in BNGL)
# the bond should be visible from the declaration
cplx = CplxInst( 
    [
        MolInst( CaMKII, [CompInst(d), CompInst(r), CompInst(l, bond=1), CompInst(Y286, 0), CompInst(S306, 0), CompInst(cam)] ) ,
        MolInst( CaMKII, [CompInst(d), CompInst(r, bond=1), CompInst(l), CompInst(Y286, 0), CompInst(S306, 0), CompInst(cam)] )
    ]
)

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
        CplxPattern( [
            MolPattern( CaMKII, [CompPattern(l), CompPattern(r), CompPattern(Y286, '0'), CompPattern(cam, bond=BOND_PLUS)] )  
        ] ),
        CplxPattern( [
            MolPattern( CaMKII, [CompPattern(l), CompPattern(r), CompPattern(cam, bond=BOND_PLUS)] )  
        ] ),
    ],
    products=[
        CplxPattern( [
            MolPattern( CaMKII, [CompPattern(l, bond=1), CompPattern(r), CompPattern(Y286, '0'), CompPattern(cam, bond=BOND_PLUS)] ),
            MolPattern( CaMKII, [CompPattern(l), CompPattern(r, bond=1), CompPattern(cam, bond=BOND_PLUS)] )
        ] )
    ]
)

print("Reaction rule:")
print(rxn)
print("")

