//
//  model.hpp
//  libmcell
//
//  Created by Oliver Ernst on 2/22/20.
//

#ifndef model_hpp
#define model_hpp

#include <stdio.h>
#include "rxn.hpp"
#include <set>

#endif /* model_hpp */

namespace mcl {

    class Model : public ModelRxnIfce {
        
    private:
        
        // Rxns
        std::set<Rxn*> _rxns;
            
        // Internal copy func/clean up
        void _clean_up();
        void _copy(const Model& other);
        void _move(Model &other);
        
    public:
                
        // ***************
        // MARK: - Constructor
        // ***************
        
        Model();
        Model(const Model& other);
        Model& operator=(const Model& other);
        Model(Model&& other);
        Model& operator=(Model&& other);
        ~Model();
        
        // ***************
        // MARK: - Reactions
        // ***************
        
        void add_rxn(Rxn* rxn);
        void remove_rxn(Rxn* rxn);
        
        // ***************
        // MARK: - ModelRxnIfce implementations
        // ***************
        
        void notify_fwd_rate_changed(Rxn* rxn, double fwd_rate);
    };
}
