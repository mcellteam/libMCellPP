from my_model import *

# Create the model
m = create_my_model()

# We can get handles again to the objects we have already created
pmca_p0 = m.get_species("pmca_p0")

# Run (simple!)
pmca_p0_counts = []
for timestep in range(0,100):

    # Run
    res = m.run_one_timestep(dt=1.0)

    # Error handling
    assert res.success

    # Store counts
    current_count = pmca_p0.get_count()
    pmca_p0_counts.append(current_count)

print(pmca_p0_counts)
