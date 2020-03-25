from my_model import *

import pandas as pd



# Write the running function
def parallel_execute(m, seed):

    # Seed
    m.set_seed(seed)

    # We can get handles again to the objects we have already created
    pmca_p0 = m.get_species("pmca_p0")

    # Run
    pmca_p0_counts = []
    for timestep in range(0,100):

        # Run
        res = m.run_one_timestep(dt=1.0)

        # Error handling
        assert res.success

        # Current count
        current_count = pmca_p0.get_count()
        pmca_p0_counts.append(current_count)

    # Write out
    df = pd.DataFrame(pmca_p0_counts, columns=["column"])
    df.to_csv("pmca_p0_%05d.csv" % seed)



if __name__ == "__main__":

    # Get a parallel runner
    runner = pymcell.ParallelRunner()

    # Create the model
    m = create_my_model()

    # Run for many seeds in parallel
    for seed in range(0,100):
        runner.run(target=parallel_execute, args=(m,seed))
