from my_model import *

# Create the model
m = create_my_model()

# We can get handles again to the objects we have already created
rxn = m.get_rxn("my rxn")

# Store reaction counts
rxn.store_counts = True

# Run (simple!)
rxn_counts = []
for timestep in range(0,100):

    # Change the reaction rate
    if timestep == 50:
        rxn.fwd_rate = 100.0

    # Run
    res = m.run_one_timestep(dt=1.0)

    # Error handling
    assert res.success==True

    # Store count
    count = rxn.get_count()
    rxn_counts.append(count)

print(rxn_counts)
