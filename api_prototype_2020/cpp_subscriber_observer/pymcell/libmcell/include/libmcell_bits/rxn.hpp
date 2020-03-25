//
//  rxn.hpp
//  libmcell
//
//  Created by Oliver Ernst on 2/22/20.
//

#ifndef rxn_hpp
#define rxn_hpp

#include <stdio.h>
#include <string>
#include <vector>
#include <set>
#include "model_rxn_ifce.hpp"

#endif /* rxn_hpp */

namespace mcl {

    class Rxn {
        
    private:
        
        // Subscribed models
        std::set<ModelRxnIfce*> _subscribed_models;
        
        // Name
        std::string _name;
        
        // Fwd rate
        double _fwd_rate;
                
        // Reactants and products
        std::vector<std::string> _reactants;
        std::vector<std::string> _products;
    
        // Internal copy func/clean up
        void _clean_up();
        void _copy(const Rxn& other);
        void _move(Rxn &other);
        
    public:
                
        // ***************
        // MARK: - Constructor
        // ***************
        
        Rxn(std::string name, double fwd_rate, std::vector<std::string> reactants, std::vector<std::string> products);
        Rxn(const Rxn& other);
        Rxn& operator=(const Rxn& other);
        Rxn(Rxn&& other);
        Rxn& operator=(Rxn&& other);
        ~Rxn();
        
        // ***************
        // MARK: - Name
        // ***************
        
        std::string get_name() const;
        
        // ***************
        // MARK: - Forward rate
        // ***************
        
        double get_fwd_rate() const;
        void set_fwd_rate(double fwd_rate);
        
        // ***************
        // MARK: - Add/remove subscribers
        // ***************
        
        void add_subscriber(ModelRxnIfce* model);
        void remove_subscriber(ModelRxnIfce* model);
    };
}
