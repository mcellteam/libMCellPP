from typing import List, Dict
from enum import Enum
from pathlib import Path
import logging

logging.basicConfig(format='%(message)s', level=logging.DEBUG)


class Orient(Enum):
    up = 1
    down = 2
    mix = 3


class Species():
    """ A type of molecule """
    def __init__(self, name: str, volume=True, dc=0.0) -> None:
        self.name = name
        self.volume = volume
        self.dc = dc
        vol_surf = "volume" if volume else "surface"
        logging.info("Creating %s species '%s'" % (vol_surf, name))


class Molecule():
    """ An instance of a species """
    def __init__(self, spec: Species, location: (int, int, int)):
        self.spec = spec
        self.location = location


class SpeciesComplex():
    """ A complex of molecules """
    def __init__(self, spec: Species) -> None:
        self.spec = spec


odict = {Orient.up:"'", Orient.down:",", Orient.mix:";"}


class Reaction():
    """ A reaction involving molecules """
    def __init__(self, reactants, products=None, reversible=False,
                 rate=0.0, name="") -> None:
        self._reactants = reactants
        self._products = products
        self._reversible = reversible
        self.rate = rate
        self.name = name
        reactant_names = [r[0].name+odict[r[1]] for r in reactants]
        reactants_str = " + ".join(reactant_names)
        if products:
            product_names = [r[0].name+odict[r[1]] for r in products]
            products_str = " + ".join(product_names)
        else:
            products_str = "NULL"
        arrow = "<->" if reversible else "->"
        logging.info("Creating reaction %s %s %s [%.2E]" % (
            reactants_str, arrow, products_str, rate))


class Rule():
    def __init__(self):
        pass


class SP(Enum):
    reflect = 1
    transp = 2
    absorb = 3
    clamp = 4


class Region():
    def __init__(self, name: str, face_indices: List[int]):
        self.name = name
        self.face_indices = face_indices
        logging.info("Creating region '%s'" % name)


class SurfaceProperty():
    """ How a species interacts with a surface (boundary) """
    def __init__(
            self, name: str, surf_type: SP, spec, clamp_val: int=None) -> None:
        self.name = name
        self.surf_type = surf_type
        logging.info("Creating surface property '%s'" % name)


class Shape(Enum):
    cube = 1
    sphere = 2


class ShapeKey():
    def __init__(self):
        pass


class MeshObject():
    def __init__(self, name: str, verts: List[int],
                 faces: List[int], regions: Dict[str, Region] = None,
                 shape_keys: ShapeKey=None) -> None:
        self.name = name
        self.verts = verts
        self.faces = faces
        self.regions = regions
        logging.info("Creating mesh object '%s'" % name)

    def add_surface_property(
            self, surf_prop: SurfaceProperty, reg: Region):
        pass


def create_box(name: str, width: float) -> MeshObject:
        logging.info("Creating box object '%s'" % name)
        regs = {
            "top": Region("top", [0, 1]),
            "bottom": Region("bottom", [2, 3]),
            "left": Region("left", [4, 5]),
            "right": Region("right", [6, 7]),
            "front": Region("front", [8, 9]),
            "back": Region("back", [10, 11]),
        }
        return MeshObject(name, [1], [1], regs)


def import_obj(obj_path: Path) -> MeshObject:
    logging.info("Importing mesh object from '%s'" % obj_path)
    return MeshObject("box", [1], [1])


class Count():
    def __init__(self):
        pass


class CountMolecules(Count):
    def __init__(self, spec: Species, location: MeshObject=None) -> None:
        self.spec = spec
        self.location = location
        logging.info("Creating count of '%s' in/on '%s'" % (
            spec.name, location.name))


class CountReaction(Count):
    def __init__(self, rxn: Reaction, location: MeshObject=None) -> None:
        self.rxn = rxn
        self.location = location
        logging.info("Creating count of '%s' in/on '%s'" % (
            rxn.name, location.name))


class Simulation():
    def __init__(
            self,
            dt: float,
            molecules: List[Molecule]=None,
            reactions: List[Reaction]=None,
            counts: List[Count]=None,
            meshes: List[MeshObject]=None) -> None:
        self.dt = dt
        self.molecules = molecules
        self.reactions = reactions
        self.counts = counts
        self.meshes = meshes

    def create_molecules_shape(
            self, spec: Species, amount: float,
            location: (float, float, float), width: float=0.0,
            shape: Shape=Shape.cube, conc=False) -> None:
        logging.info("Creating %g '%s' molecules at %s" % (
            amount,
            spec.name,
            location))

    def create_molecules_obj(self, spec: Species, obj: MeshObject,
            amount: float, conc=False, orient: Orient=None) -> None:
        logging.info("Creating %g '%s' molecules on/in '%s'" % (
            amount,
            spec.name,
            obj.name))

    def create_molecules_reg(self, spec: Species, reg: Region, amount: float,
                             conc_dens=False, orient: Orient=None) -> None:
        logging.info("Creating %g '%s' molecules on/in '%s'" % (
            amount,
            spec.name,
            reg.name))

    def run_iteration(self) -> None:
        pass

    def run_iterations(self, iterations) -> None:
        logging.info("Running %d iterations" % iterations)
        for i in range(iterations):
            self.run_iteration()
