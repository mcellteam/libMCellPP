#!/usr/bin/env python3.4


class _species_class:
  def __init__(self,name=None, type='VOL', diffusion_constant=0.0, target_only=False, custom_timestep=None, custom_spacestep=None, components=None):
    self.name = name
    self.type = type
    self.diffusion_constant = diffusion_constant
    self.target_only=target_only
    self.custom_timestep=custom_timestep
    self.custom_spacestep=custom_spacestep
    self.components=components


class mcell_world:

  class _species:
    def get(self, key):
      return self.species.__dict__[key]

  def __init__(self):
    self.species = self._species()

  def add_species(self,key,val):
    self.species.__dict__[key] = type(key, (_species_class,), {})(key)

  def remove_species(self,key):
    self.species.__dict__.pop(key)
