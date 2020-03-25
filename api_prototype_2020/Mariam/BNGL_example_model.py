import pymcell

class MySpecies(Species):
    pass

    def get_count(self):
        model.get_geometry().count(self)

class BNGRxn(Rxn):

    def init(self, ...):
        pass

def create_my_model():

    #Some parameters:
    V = 0.125*1e-15 # um^3 -> liters
    NA = 6.022e23/1e6
    #Rate Constants (The numbers used here are taken from the SBML file available online)
    k_on1C = 4/(NA*V) #1/uM 1/s 
    k_off1C = 40 #1/s (10-70)
    k_on2C = 10/(NA*V) #1/uM 1/s 
    k_off2C = 9.25 #1/s (8.5-10)    
    k_on1N = 100/(NA*V) #1/uM 1/s 
    k_off1N = 2500 #1/s
    k_on2N = 150/(NA*V) #1/uM 1/s 
    k_off2N = 750 #1/s 

    k_onCaM1C1N = 3.3/(NA*V) #1/uM 1/s 
    k_offCaM1C1N = 3.4 #1/s

    k_onCaMKII = 50/(NA*V) #1/uM 1/s 
    k_offCaMKII = 60 #1/s 

    k_pCaM1C1N = 0.094 #1/s 

    

    # Add some geometries
    a001 = pymcell.Geometry.fromFile("a001.ply")
    print(a001)

    C = pymcell.Sites(
        states = [0,1,2]
        )
    N = pymcell.Sites(
        states = [0,1,2]
        )
    Y286 = pymcell.Sites(
        states = ['0','P']
        )
    b_site = pymcell.Sites(
        states = [0,1]
        int bond_N = 0
        ) # the way I envision this whenver bond_N > 1 (optional feature, present only for binding sutes) states becomes 1 

    ca = pymcell.Species(
        name="ca",
        diff_const=10.0
        )


    CaM = pymcell.Species(
        name = "CaM",
        diff_const =10.0,
        sites = [C,N,b_site]
        )
    CaMKII = pymcell.Species(
        name = "CaM",
        diff_const =10.0,
        sites = [b_site,Y286,rb_site,lb_site]
        )
    Complex = pymcell.Complex(
        name = "Complex",
        components = [],
        diff_const =10.0, # calculated from components?
        )
    bng_rxn = BNGRxn(...)


    rxn_volume = pymcell.Rxn(
        name="first rxn",
        fwd_rate=k_on1C,
        bkwd_rate=k_off1C,
        reactants=[
            CaM(sites(C[0],b_stie.state[0])),
            ca
        ],
        products=[
            CaM(sites(C[1],b_stie.state[0]))
        ]
    )

    rxn_volume = pymcell.Rxn(
        name="second rxn",
        fwd_rate=k_on2C,
        bkwd_rate=k_off2C,
        reactants=[
            CaM(sites(C[1],b_stie.state[0])),
            ca
        ],
        products=[
            CaM(sites(C[2],b_stie.state[0]))
        ]
    )

    rxn_volume = pymcell.Rxn(
        name="third rxn",
        fwd_rate=k_on1N,
        bkwd_rate=k_off1N,
        reactants=[
            CaM(sites(N[0],b_stie.state[0])),
            ca
        ],
        products=[
            CaM(sites(N[1],b_stie.state[0]))
        ]
    )
    rxn_volume = pymcell.Rxn(
        name="fourth rxn",
        fwd_rate=k_on2N,
        bkwd_rate=k_off2N,
        reactants=[
            CaM(sites(N[1],b_stie.state[0])),
            ca
        ],
        products=[
            CaM(sites(N[2],b_stie.state[0]))
        ]
    )

    rxn_volume = pymcell.Rxn(
        name="fifth rxn",
        fwd_rate=k_onCaM1C1N,
        bkwd_rate=k_offCaM1C1N,
        reactants=[
            CaM(sites(C[1],N[1],b_stie.state[0])),
            CaMKII(sites(b_stie.state[0],Y286['0']))
        ],
        products=[
            Complex(components = [CaM(sites(C[1],N[1],b_site.N_bond=1)),CaMKII(sites(b_site.N_bond=1,Y286['0']))])
        ]
    )

    rxn_volume = pymcell.Rxn(
        name="sixth rxn",
        fwd_rate=k_onCaMKII,
        bkwd_rate=k_offCaMKII
        reactants=[
            Complex(components = [
                CaMKII(sites(b_site.state[1],Y286['0'],rb_stie.state[0],lb_stie.state[0])),
                ])
            Complex(components =[
                CaMKII(sites(b_site.state[1],rb_stie.state[0],lb_stie.state[0]))
            ])
        ]
        products=[
            Complex(components = [
                CaMKII(sites(b_site.state[1],Y286['0'],lb_site.bond_N=1,rb_stie.state[0])),
                CaMKII(sites(b_site.state[1],lb_stie.state[0],rb_site.bond_N=1))
            ])
        ]
    )


    rxn_volume = pymcell.Rxn(
        name="seventh rxn",
        fwd_rate=k_pCaM1C1N,
        reactants=[
            Complex(components = [
                CaMKII(sites(b_site.state[1],Y286['0'],lb_site.bond_N=1)),
                CaM(sites(C[1],N[1],b_site.bond_N=2)),
                CaMKII(sites(b_site.bond_N=2,Y286['0'],rb_site.bond_N=1))
            ])
        ]
        products=[
            Complex(components = [
                CaM,
                CaMKII(sites(b_site.state[1],Y286['0'],lb_site.bond_N=1)),
                CaM(sites(C[1],N[1],b_site.bond_N=2)),
                CaMKII(sites(b_site.bond_N=2,Y286['P'],rb_site.bond_N=1))
            ])
        ]
    )

    # Create releases
    release_1 = pymcell.ReleaseSite(
        name="Ca",
        type=pymcell.RELEASE_TYPE.OBJECT,
        species=ca,
        quantity=10*(NA*V),
        release_probability=1,
        object=a001.get_volume_region("dendritic_spine")
    )
    release_2 = pymcell.ReleaseSite(
        name="CaM",
        type=pymcell.RELEASE_TYPE.OBJECT,
        species=CaM(sites(C[0],N[0],b_stie.state[0])),
        quantity=30*(NA*V),
        release_probability=1,
        object=a001.get_volume_region("dendritic_spine")
    )
    release_3 = pymcell.ReleaseSite(
        name="CaMKII",
        type=pymcell.RELEASE_TYPE.OBJECT,
        species=CaMKII(sites(b_stie.state[0],Y286['0'],rb_stie.state[0],lb_stie.state[0])),
        quantity=80*(NA*V),
        release_probability=1,
        object=a001.get_volume_region("dendritic_spine")
    )
    # Finally: add all that to a model
    m = pymcell.Model()
    m.add_geometry(a001)
    m.add_species(ca)
    m.add_species(CaM)
    m.add_species(CaMKII)
    m.add_rxn(rxn_volume)
    m.add_release_site(release_1,release_2,release_3)


    m.add_rxn(bng_rxn)


    return m
