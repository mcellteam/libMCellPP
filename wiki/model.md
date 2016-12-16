# What is an MCell data model (i.e. simulation)?

This page attempts to describe a discussion on (12/13) between Tom/Bob/Oliver regarding what a data model fundamentally is, and how it could be set up to allow collaborative projects. Please change/edit/delete liberally.

Also: this document also blends the concept of the data model and the simulation model - this may not be correct!

A data model is a dictionary.

This makes sharing and collaborating on models natural using submodels. Consider making a new model in pyMCell via
```
my_model = m.create_model()
```

This creates a dictionary similar to the following (not necessarily these keys - TO BE CHANGED!):

![model_namespace](./figures/model_namespace.jpg?raw=true "An MCell model")

This model lives in the local namespace, and may be accessed within this script by e.g. some code similar to the following:
```
my_model.species.species_A
```

or run using e.g.
```
my_model.run_iteration()
```

Consider now collaborating on a project. Your collaborator gives you the file `other_file` which contains the data model `my_other_model`. You can import it via:
```
import other_file
```

This gives:

![model_namespace_import](./figures/model_namespace_import.jpg?raw=true "Two models")

You can now access the new model using the natural python syntax:
```
other_file.my_other_model.species.species_A
other_file.my_other_model.run_iteration()
```

Currently this model is **totally separate** from `my_model`. Running an iteration in `other_file.my_other_model` does not run an iteration in `my_model`. Furhermore, the particles can't see objects that are in different models, etc.

To join the two models, the user could type a command similar to something like:
```
my_model.add_submodel(other_file.my_other_model)
```

This should create the following structure:

![model_joined](./figures/model_joined.jpg?raw=true "Submodels")

Particles can now see each other, react with each other, interact with objects in the other parts of the model, etc.

Now, the user can access parameters in the original model as before, using:
```
my_model.species.species_A
```

but also in `my_other_model` using:
```
my_model.my_other_model.species.species_A
```

At runtime, there is a naming conflict - species_A exists in both the original model, and the submodel. This can be resolved by systematic naming. Two species are created: (1) named `species_A`, defined by the original model, and (2) named `my_other_model.species_A` defined by the submodel.

