# List of Example Usage Cases for the API

1. Unbounded diffusion
2. "1D diffusion" in a thin tube
	* initial release in a plane in the middle
3. "2D diffusion" between two sheets
	* initial release in a line source
4. 2D diffusion on a real 2D surface
	* initial release on a patch by either density or Boolean intersection of e.g. a sphere with a plane
5. Volumetric diffusion in a box/sphere
6. Box of A & B with reactions:
	* A -> 0 decay
	* A -> B decay
	* A + B -> C irreversible
	* A + B <-> C reversible
7. Box of A & B with reactions on a surface:
	* A (volumetric) + B (surface) -> C (surface)
8. Surface classes
	* Box with one transparent side to molecule A
	* Box with absorptive side to molecule A
	* Box with concentration clamp of A on one side and absorptive on the opposing side
9. Object with a generally complex geometry from some list of vertices and faces
10. Dynamic changes
	* Dynamic geometry: an interface to change the mesh at each timestep
		* Example: An initial box that updates it's geometry at each timestep with some new list of vertices and faces
	* Dynamic rate constants: changing the rate constant of a reaction
		* Example: A box with A+B->C that where the rate constant depends on the number of A,B, or C
	* Dynamic diffusion constants: changing the diffusion constant for a molecule
		* Example: A box of diffusing A particles that increase their diffusion constants over time
11. Counting statements
	* A box (maybe with some region definition) with A+B->C reaction where we count each of the following at each timestep:
		* What: molecule, reaction, event/trigger
		* Where: World, object, region
		* When: frequency of counting
		* How: Front hits/back hits, e.g. on a plane that goes through the box
12. SubClassing Molecule Species
	* Implement a subclass of molecule that occupies space
13. SubClassing Molecules and Reactions
	* Implement subclasses that use BioNetGen-like molecules and reactions
14. SubClassing Diffusion
	* Implement a subclass that uses a different kind of diffusion
15. SubClassing the Scheduler
	* Implement a subclass that uses a variable time-step scheduler



