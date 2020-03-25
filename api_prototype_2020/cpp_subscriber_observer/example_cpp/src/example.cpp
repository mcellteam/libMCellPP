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
        
    // A + B -> C
    auto rxn = Rxn("my rxn", 1.0, {"A"}, {"B", "C"});

    // Make a model
    auto model = Model();

    // Add rxn
    model.add_rxn(&rxn);
    
    // Change the reaction rate
    rxn.set_fwd_rate(3.0);
    
    return 0;
}
