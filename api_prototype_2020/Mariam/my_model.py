import pymcell

class MySpecies(Species):
    pass

    def get_count(self):
        model.get_geometry().count(self)

class BNGRxn(Rxn):

    def init(self, ...):
        pass

def create_my_model():

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
        )

    # # Make a species
    # pmca_p0 = pymcell.Species(
    #     name="pmca_p0",
    #     diff_const=10.0
    #     )
    # pmca_po.set_diff_const(5)

    ca = pymcell.Species(
        name="ca",
        diff_const=10.0
        )

    # pmca_p1 = pymcell.Species(
    #     name="pmca_p1",
    #     diff_const=10.0
    #     )

    CaM = pymcell.Species(
        name = "CaM",
        diff_const =10.0,
        states = [C,N,b_site]
        )
    CaMKII = pymcell.Species(
        name = "CaM",
        diff_const =10.0,
        states = [b_site,Y286]
        )
    Complex = pymcell.Complex(
        name = "Complex",
        components = [],
        diff_const =10.0, # calculated from components?
        )
    bng_rxn = BNGRxn(...)

    # Make a surface reaction
    # pmca_p0' + ca, <-> pmca_p1'
    # rxn_surface = pymcell.Rxn(
    #     name="first rxn",
    #     fwd_rate=1.0,
    #     bkwd_rate=2.0,
    #     reactants=[
    #         pymcell.oriented_species(pmca_p0, pymcell.ORIENT.UP),
    #         pymcell.oriented_species(ca, pymcell.ORIENT.DOWN)
    #     ],
    #     products=[
    #         pymcell.oriented_species(pmca_p1, pymcell.ORIENT.UP)
    #     ]
    # )

    # Make a volume reaction
    # calbindin_h0m0 + ca <-> calbindin_h1m0
    # rxn_volume = pymcell.Rxn(
    #     name="second rxn",
    #     fwd_rate=1.0,
    #     bkwd_rate=2.0,
    #     reactants=[
    #         calbindin_h0m0,
    #         ca
    #     ],
    #     products=[
    #         calbindin_h1m0
    #     ]

    rxn_volume = pymcell.Rxn(
        name="third rxn",
        fwd_rate=1.0,
        bkwd_rate=2.0,
        reactants=[
            CaM(states(C[0],b_site[0])),
            ca
        ],
        products=[
            CaM(states(C[1],b_site[0]))
        ]
    )

    rxn_volume = pymcell.Rxn(
        name="third rxn",
        fwd_rate=1.5,
        bkwd_rate=1.5,
        reactants=[
            CaM(states(C[1],b_site[0])),
            ca
        ],
        products=[
            CaM(states(C[2],b_site[0]))
        ]
    )

    rxn_volume = pymcell.Rxn(
        name="fourth rxn",
        fwd_rate=1.0,
        bkwd_rate=2.0,
        reactants=[
            CaM(states(C[0],b_site[0])),
            CaMKII(states(b_site[0],Y286[0]))
        ],
        products=[
            Complex(components = [CaM(states(C[1],b_site[1])),CaMKII(states(b_site[1],Y286[0]))])
        ]
    )
    rxn_volume = pymcell.Rxn(
        name="fourth rxn",
        fwd_rate=1.0,
        reactants=[
            Complex(components = [
                CaM,
                CaMKII(states(b_site[1],Y286[0],d_site[1])),
                CaM(states(C[1],N[2],b_site[1])),
                CaMKII(states(b_site[1],Y286[0],d_site[1]))
            ])
        ]
        products=[
            Complex(components = [
                CaM,
                CaMKII(states(b_site[1],Y286[0],d_site[1])),
                CaM(states(C[1],N[2],b_site[1])),
                CaMKII(states(b_site[1],Y286[P],d_site[1]))
            ])
        ]
    )

    # Create releases
    release_1 = pymcell.ReleaseSite(
        name="pmca_p0_pre_rel",
        type=pymcell.RELEASE_TYPE.OBJECT,
        species=pmca_p0,
        quantity=100,
        release_probability=1,
        object=a001.get_surface_region("axon_membrane")
    )
    release_2 = CaM.ReleaseSite(
        name="pmca_p0_pre_rel",
        type=pymcell.RELEASE_TYPE.OBJECT,
        species=CaM(CaM_states(C[0],N[0],Y286[0])),
        quantity=100,
        release_probability=1,
        object=a001.get_volume_region("dendritic_spine")
    )

    # Finally: add all that to a model
    m = pymcell.Model()
    m.add_geometry(a001)
    m.add_species(pmca_p0)
    m.add_species(ca)
    m.add_species(pmca_p1)
    m.add_rxn(rxn_volume)
    m.add_rxn(rxn_surface)
    m.add_release_site(release_1)

    m2 = pymcell.Model()
    m2.add_geometry(a001)
    m2.add_species(pmca_p0)
    m2.add_species(ca)
    m2.add_species(pmca_p1)
    m2.add_rxn(rxn_volume)
    m2.add_rxn(rxn_surface)
    m2.add_release_site(release_1)

    m.add_rxn(bng_rxn)


    return m
