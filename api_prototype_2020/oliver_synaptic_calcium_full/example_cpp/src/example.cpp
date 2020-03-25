//
//  example.cpp
//  example
//
//  Created by Oliver Ernst on 2/22/20.
//

#include <stdio.h>
#include <libmcell>

using namespace std;
using namespace mcl;

int main() {
        
    // Species
    auto species_A = Species("A", 1.0);
    auto species_B = Species("B", 1.0);
    auto species_C = Species("C", 1.0);

    
    // A + B -> C
    auto rxn = Rxn("my rxn", 1.0, {&species_A}, {&species_B, &species_C});

    // Make a model
    double dt = 0.1;
    auto model = Model(dt);

    // Add species
    model.add_species(&species_A);
    model.add_species(&species_B);
    model.add_species(&species_C);
    
    // Add rxn
    model.add_rxn(&rxn);
    
    // Run
    for (size_t timestep=0; timestep<10; timestep++) {
        
        // Run
        auto result = model.run_timestep();
        assert (result.get_success() == true);
        
        // Change something...
        if (model.get_timepoint() == 5) {
            
            // Change the reaction rate
            rxn.set_fwd_rate(3.0);
            
        }
    };
    
    return 0;
}
