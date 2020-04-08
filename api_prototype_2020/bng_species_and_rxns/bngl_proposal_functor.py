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

class ComponentType:
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

    # called when the object is called as a function
    # creates an instance from a previously created template 
    def __call__(self, state=STATE_UNSET, bond=BOND_NONE):
        return ComponentInstance(self, state, bond)

    # prints out the declaration of the component in BNGL (template information)
    def __str__(self):
        res = self.name
        
        for s in self.allowed_states:
            res += '~' + s  

        return res


class ComponentInstance:
    def __init__(self, component_type: ComponentType, state:str=STATE_UNSET, bond:int=BOND_NONE):
        self.component_type = component_type
        self.bond = bond
        self.state = STATE_UNSET
        
        state = str(state)
        # set component state
        if state != STATE_UNSET:
            if state not in self.component_type.allowed_states:
                msg = 'ComponentType ' + self.component_type.name + ': state ' + state + ' is not in allowed states ' + str(self.allowed_states) + '.'
                raise ValueError(msg)
            else:
                self.state = state

    
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
        
class MoleculeType:
    def __init__(self, diff_const, name = '', components=[]):
        # name, diff_const, and all_components serve for component template
        if name: 
            self.name = name
        else:
            self.name = varname() # store the name of the created object variable (maintained with shallow copy)
        self.diff_const = diff_const
        
        self.components = []
        for ct in components:
            if type(ct) != ComponentType:
                raise ValueError('Only objects of ComponentType can be passed as MoleculeType components.')        
            self.components.append(ct)        
        self.all_components = components
        

    def __call__(self, *args):
        return MoleculeInstance(self, *args)
    
        
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
        
        
class MoleculeInstance:
    def __init__(self, molecule_type: MoleculeType, *args):
        self.molecule_type = molecule_type
        
        self.components = []
        for ci in args:
            if type(ci) != ComponentInstance:
                raise ValueError('Only objects of ComponentInstance can be passed as MoleculeInstance components.')        
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
        
        
# used in reactions as reactants and products as a matching pattern       
class ComplexInstance:
    def __init__(self, *args):
        self.molecule_types = []
        
        for v in args:
            if type(v) != MoleculeInstance:
                raise ValueError('Only objects of MoleculeInstance can be passed as Complex constructor arguments.')        
            self.molecule_types.append(v)
            
            
    def __str__(self):      
        res = ''
        
        num_molecule_types = len(self.molecule_types)
        for i in range(num_molecule_types):
            res += str(self.molecule_types[i])
            if i != num_molecule_types-1:
                res += '.' 
        return res
        
            
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

C = ComponentType(   
    states = [0,1,2]
)

print("ComponentType declaration:")
print(C)   
print("")

N = ComponentType(
    states = [0,1,2]
)
ng = ComponentType()
camkii = ComponentType()



Y286 = ComponentType(
    states = ['0','P']
)


CaM = MoleculeType(
    diff_const =10.0,
    components = [C, N]
)

# -------------------------  CaMKII --------------



d = ComponentType() # no states  
l = ComponentType()
r = ComponentType()
Y286 = ComponentType(
    states = ['0','P']
)
S306 = ComponentType(
    states = ['0','P']
)
cam = ComponentType()


CaMKII = MoleculeType(
    diff_const =10.0,
    components = [d, r, l, Y286, S306]    
)
    
print("Molecule type declaration:")
print(CaM)
print("")
    
print("Molecule type declaration:")
print(CaMKII)
print("")

mol_type_inst = CaMKII( d(), r(), l(), Y286(0), S306(0), cam() )

print("Molecule type instance:")
print(mol_type_inst)
print("")

# this is already an instance of a complex
# serves as a pattern when used in a reaction
cplx = ComplexInstance( 
    # Y286('0') means Y286~0
    CaMKII( d(), r(), l(bond=1), Y286(0), S306(0), cam() ),
    CaMKII( d(), r(bond=1), l(), Y286(0), S306(0), cam() )
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
        ComplexInstance( 
            CaMKII( l(), r(), Y286('0'), cam(bond=BOND_PLUS) ) 
        ),
        ComplexInstance( 
            CaMKII( l(), r(), cam(bond=BOND_PLUS) ) 
        )
    ], 
    products=[
        ComplexInstance( 
            CaMKII( l(bond=1), r(), Y286('0'), cam(bond=BOND_PLUS) ),
            CaMKII( l(), r(bond=1), cam(bond=BOND_PLUS) )
        )
    ]
)


print("Reaction rule:")
print(rxn)
print("")


