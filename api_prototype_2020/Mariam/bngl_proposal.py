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
            
        self.allowed_states = []  
        for s in states:
            self.allowed_states.append(str(s))
        
        # specific state and bond is set when this template is 'specialized/instanced' 
        self.state = STATE_UNSET  # string
        self.bond = BOND_NONE      # integer


    # called when the object is called as a function
    # creates an instance from a previously created template 
    def __call__(self, state=STATE_UNSET, name='', bond=BOND_NONE):
        
        # convert state name to string if integer was passed
        state = str(state)
        
        # we need to create a copy of our object to do modifications and then return it
        # deepcopy is safer to use, we do not want to end up unexpectingly overwriting data of other 
        # components or molecule types   
        res = copy.deepcopy(self)
        
        # override name if it was set
        if name: 
            res.name = name
            
        # set component state
        if state != STATE_UNSET:
            if state not in self.allowed_states:
                msg = 'ComponentType ' + self.name + ': state ' + state + ' is not in allowed states ' + str(self.allowed_states) + '.'
                raise ValueError(msg)
            else:
                self.state = state
                
        # we always use the bond value when creating instance
        res.bond = bond
                
        return res

    # prints out the declaration of the component in BNGL (template information)
    def to_decl_str(self):
        res = self.name
        
        for s in self.allowed_states:
            res += '~' + s  

        return res
        
    # prints out speicifc instance information
    def __str__(self):
        res = self.name
        
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
        self.all_components = components
        
        # components are specific components set when this molecule type is used in a complex
        self.components = []
        
    # called when the object is called as a function
    # creates an instance from a previously created template 
    def __call__(self, *args):
        self.molecule_types = []

        res = copy.deepcopy(self)

        for v in args:
            if type(v) != ComponentType:
                raise ValueError('Only objects of ComponentType can be passed when specializing a MoleculeType.')        
            res.components.append(v)    
        
        # note: here could be a check that the components that we got are a subset of all_components,
        # but it would be probably better to do semantic checks in C++ code
        return res 
        
    # prints out the declaration of the component in BNGL (template information)  
    def to_decl_str(self):
        res = self.name + '('
        
        num_components = len(self.all_components)
        for i in range(num_components):
            res += self.all_components[i].to_decl_str()
            if i != num_components-1:
                res += ',' 
        
        res += ')'
        return res        
                
    # prints out speicifc instance information                
    def __str__(self):
        res = self.name + '('
        
        num_components = len(self.components)
        for i in range(num_components):
            res += str(self.components[i])
            if i != num_components-1:
                res += ',' 
        
        res += ')'
        return res
        
        
# used in reactions as reactants and products as a matching pattern       
class Complex:
    def __init__(self, *args):
        self.molecule_types = []
        
        for v in args:
            if type(v) != MoleculeType:
                raise ValueError('Only objects of MoleculeType can be passed as Complex constructor arguments.')        
            self.molecule_types.append(v)
            
            
    def __str__(self):      
        res = ''
        
        num_molecule_type = len(self.molecule_types)
        for i in range(num_molecule_type):
            res += str(self.molecule_types[i])
            if i != num_molecule_type-1:
                res += '.' 
        return res
        
            
class RxnRule:
    def __init__(self):
        #TODO
        pass
    
    def __str__(self):      
        #TODO
        pass
            
    
C = ComponentType(   
    states = [0,1,2]
)

N = ComponentType(
    states = [0,1,2]
)

Y286 = ComponentType(
    states = ['0','P']
)

print("ComponentType declaration:")
print(C.to_decl_str())   
print("")


b = ComponentType() # no states  
l = ComponentType()
r = ComponentType()


CaM = MoleculeType(
    diff_const =10.0,
    components = [C(), N()]
)

CaMKII = MoleculeType(
    diff_const =10.0,
    # we need to specify new names for our components
    components = [b(), Y286(), r(), l()]    
)
    
print("Molecule type declaration:")
print(CaM.to_decl_str())
print("")
    
print("Molecule type declaration:")
print(CaMKII.to_decl_str())
print("")

mol_type_inst = CaMKII( b(), l(), r() )

print("Molecule type instance:")
print(mol_type_inst)
print("")

# this is already an instance of a complex
# serves as a pattern when used in a reaction
cplx = Complex( 
    # Y286('0') means Y286~0
    CaMKII( b(), Y286('0'), l(bond=1), r() ),
    CaMKII( b(), l(), r(bond=1) )
)

print("Complex instance:")
print(cplx)
print("")



"""
V = 0.125*1e-15 # um^3 -> liters
NA = 6.022e23/1e6
k_onCaMKII = 50/(NA*V) #1/uM 1/s 
k_offCaMKII = 60 #1/s 

    
rxn_volume = RxnRule(
    name="sixth rxn",
    fwd_rate=k_onCaMKII,
    bkwd_rate=k_offCaMKII,
    reactants=[
        Complex( 
            
            # the states 0 or 1 for b_comp, r_comp and l_com should probably not be there - the orig decl has no states either   
            # it does not matter whether one uses Y286('0') or Y286(0) - all state names are converted to strings
            CaMKII( b_comp(1), Y286('0'), r_comp(0), l_comp(0) ) 
        ), 
        Complex(
            CaMKII( b_comp(1), r_comp(0), l_comp(0) )
        )
    ],
    products=[
        Complex(
            # question: the components are in a different order here than in the reactants, is this allowed? 
            CaMKII( b_comp(1), Y286('0'), l_comp(0, bond=1), r_comp(0)),
            CaMKII( b_comp(1), l_comp(0), r_comp(0, bond=1))
        )
    ]
)

"""

# possible tasks 1) print the original BNGL reaction string

# print(rxn_volume)  

# then one can possibly try to modify the definition according to the bngl_example_model.bngl to see how it would look like 
