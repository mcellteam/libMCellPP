//
//  rxn.hpp
//  libmcell
//
//  Created by Oliver Ernst on 2/22/20.
//

#ifndef rxn_hpp
#define rxn_hpp

#include "model_rxn_ifce.hpp"
#include "species.hpp"

#include <stdio.h>
#include <string>
#include <vector>
#include <set>

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
        
        // Whether backward rate exists
        bool _bkwd_rate_exits;
        double _bkwd_rate;
        
        // Reactants and products
        std::vector<Species*> _reactants;
        std::vector<Species*> _products;
    
        // Internal copy func/clean up
        void _clean_up();
        void _copy(const Rxn& other);
        void _move(Rxn &other);
        
    public:
                
        // ***************
        // MARK: - Constructor
        // ***************
        
        Rxn(std::string name, double fwd_rate, std::vector<Species*> reactants, std::vector<Species*> products);
        Rxn(std::string name, double fwd_rate, double bkwd_rate, std::vector<Species*> reactants, std::vector<Species*> products);
        Rxn(const Rxn& other);
        Rxn& operator=(const Rxn& other);
        Rxn(Rxn&& other);
        Rxn& operator=(Rxn&& other);
        ~Rxn();
        
        // ***************
        // MARK: - Add/remove subscribers
        // ***************
        
        void add_subscriber(ModelRxnIfce* model);
        void remove_subscriber(ModelRxnIfce* model);
        
        // ***************
        // MARK: - Name
        // ***************
        
        std::string get_name() const;
        
        // ***************
        // MARK: - Rxn rates
        // ***************
        
        double get_fwd_rate() const;
        void set_fwd_rate(double fwd_rate);
        
        bool check_bkwd_rate_exists() const;
        double get_bkwd_rate() const;
        void set_bkwd_rate(double bkwd_rate);
        
        // ***************
        // MARK: - Reactants and products
        // ***************
        
        std::vector<Species*> get_reactants() const;
        std::vector<Species*> get_products() const;
    };
}
