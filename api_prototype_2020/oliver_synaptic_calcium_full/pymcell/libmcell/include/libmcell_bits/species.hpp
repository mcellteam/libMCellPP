//
//  species.hpp
//  pymcell
//
//  Created by Oliver Ernst on 2/23/20.
//

#ifndef species_hpp
#define species_hpp

#include "model_species_ifce.hpp"

#include <stdio.h>
#include <string>
#include <set>

#endif /* species_hpp */

namespace mcl {

    class Species {
        
    private:
    
        // Subscribed models
        std::set<ModelSpeciesIfce*> _subscribed_models;

        // Name
        std::string _name;
        
        // Diffusion constant
        double _diff_const;
            
        // Internal copy func/clean up
        void _clean_up();
        void _copy(const Species& other);
        void _move(Species &other);
        
    public:
                
        // ***************
        // MARK: - Constructor
        // ***************
        
        Species(std::string name, double diff_const);
        Species(const Species& other);
        Species& operator=(const Species& other);
        Species(Species&& other);
        Species& operator=(Species&& other);
        ~Species();
        
        // ***************
        // MARK: - Add/remove subscribers
        // ***************
        
        void add_subscriber(ModelSpeciesIfce* model);
        void remove_subscriber(ModelSpeciesIfce* model);
        
        // ***************
        // MARK: - Name
        // ***************
        
        std::string get_name() const;
        
        // ***************
        // MARK: - Diffusion constant
        // ***************
        
        double get_diff_const() const;
        void set_diff_const(double diff_const);
    };
}
