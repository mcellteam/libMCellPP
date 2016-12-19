from typing import List
from enum import Enum
from pathlib import Path


class Species():
    """ A type of molecule """
    def __init__(self, name: str, volume=True, dc=0.0) -> None:
        self.name = name
        self.volume = volume
        self.dc = dc


class Molecule():
    """ An instance of a species """
    def __init__(self, spec: Species, location: (int, int, int)):
        self.spec = spec
        self.location = location


class SpeciesComplex():
    """ A complex of molecules """
    def __init__(self, spec: Species) -> None:
        self.spec = spec


class Reaction():
    """ A reaction involving molecules """
    def __init__(self, reactants: List[Species],
                 products: List[Species]=None, reversible=False,
                 rate=0.0, name="") -> None:
        self._reactants = reactants
        self._products = products
        self._reversible = reversible
        self.rate = rate


class Rule():
    def __init__(self):
        pass


class SurfacePropertyType(Enum):
    reflective = 1
    transparent = 2
    absorptive = 3


class Region():
    def __init__(self, name: str, face_indices: List[int]):
        self.name = name
        self.face_indices = face_indices


class SurfaceProperty():
    """ How a species interacts with a surface (boundary) """
    def __init__(self, name: str, surf_type: SurfacePropertyType,
                 spec: Species, regions: List[Region]) -> None:
        self.name = name
        self.surf_type = surf_type
        self.regions = regions


class Shape(Enum):
    cube = 1
    sphere = 2


class ShapeKey():
    def __init__(self):
        pass


class MeshObject():
    def __init__(self, name: str, verts: List[int],
                 faces: List[int], regions: List[Region] = None,
                 shape_keys: ShapeKey=None) -> None:
        self.name = name
        self.verts = verts
        self.faces = faces
        self.regions = regions

    def add_surface_property(
            self, surf_prop: SurfaceProperty, indices: List[int]):
        pass


def import_obj(obj_path: Path) -> MeshObject:
    pass


class Count():
    def __init__(self):
        pass


class CountMolecules(Count):
    def __init__(self, spec: Species, location: MeshObject=None) -> None:
        self.spec = spec
        self.location = location


class CountReaction(Count):
    def __init__(self, rxn: Reaction, location: MeshObject=None) -> None:
        self.rxn = rxn
        self.location = location


class Simulation():
    def __init__(self, dt: float, molecules: List[Molecule]=None,
                 reactions: List[Reaction]=None, counts: List[Count]=None,
                 meshes: List[MeshObject]=None) -> None:
        self.dt = dt
        self.molecules = molecules
        self.reactions = reactions
        self.counts = counts
        self.meshes = meshes
        self.molecules = molecules


    def create_molecules_shape(
            self, spec: Species, amount: float,
            location: (float, float, float), width: float=0.0, 
            shape: Shape=Shape.cube, conc=False) -> None:
        pass


    def create_molecules_obj(self, spec: Species, obj: MeshObject,
                             amount: float, conc=False) -> None:
        pass


    def create_molecules_reg(self, spec: Species, reg: Region, amount: float,
                             conc=False) -> None:
        pass


    def run_iteration(self) -> None:
        pass


    def run_iterations(self, iterations) -> None:
        for i in range(iterations):
            self.run_iteration()
