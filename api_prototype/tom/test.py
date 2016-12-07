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


class myclass:

  class yy:
    def __init__(self):
      self.b = 'b'

  class _species:
    pass

  def __init__(self):
    self.y = self.yy()
    self.species = self._species()

  def add_feature(self,key,val):
    self.__dict__[key] = val

  def remove_feature(self,key):
    self.__dict__.pop(key)

  def add_class_feature(self,key,val):
    self.__class__.__dict__[key] = val

  def remove_class_feature(self,key):
    self.__class__.__dict__.pop(key)
    self.__dict__.pop(key)

  def add_species(self,key,val):
    self.species.__dict__[key] = type(key, (_species_class,), {})()

  def remove_species(self,key):
    self.__dict__.pop('species_' + key)
