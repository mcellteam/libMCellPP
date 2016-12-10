# General Notes

## Checks for objects

Objects need to be checked if they're watertight and manifold. This could be done immediately when they are added to the model:
```
box = model.create_simple_object(name="My box", type="CUBE", center=[0,0,0], radius=[1,1,1]) # Here we check, if it fails, issue an error
```

## Number of iterations

MCell currently has a number of iterations parameter - perhaps this is not necessary. The user can decide at runtime to advance step-by-step, or multiple steps at once.