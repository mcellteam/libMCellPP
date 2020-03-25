//
//  model.hpp
//  libmcell
//
//  Created by Oliver Ernst on 2/22/20.
//

#ifndef model_hpp
#define model_hpp

#include "rxn.hpp"
#include "geometry.hpp"
#include "result_timestep.hpp"

#include <stdio.h>
#include <set>

#endif /* model_hpp */

namespace mcl {

    class Model : public ModelRxnIfce, public ModelSpeciesIfce, public ModelGeometryIfce {
        
    private:
        
        // Timestep
        int _timepoint;
        double _dt;
        
        // Species
        std::set<Species*> _species;
        
        // Rxns
        std::set<Rxn*> _rxns;
        
        // Geometries
        std::set<Geometry*> _geometries;
            
        // Internal copy func/clean up
        void _clean_up();
        void _copy(const Model& other);
        void _move(Model &other);
        
    public:
                
        // ***************
        // MARK: - Constructor
        // ***************
        
        Model(double dt);
        Model(const Model& other);
        Model& operator=(const Model& other);
        Model(Model&& other);
        Model& operator=(Model&& other);
        ~Model();
        
        // ***************
        // MARK: - Run timestep
        // ***************
        
        ResultTimestep run_timestep();
        
        // ***************
        // MARK: - Timestep
        // ***************
        
        int get_timepoint() const;
        void set_timepoint(int timepoint);
        
        double get_dt() const;
        void set_dt(double dt);
        
        // ***************
        // MARK: - Species
        // ***************
        
        void add_species(Species* species);
        void remove_species(Species* species);
        
        // ***************
        // MARK: - Reactions
        // ***************
        
        void add_rxn(Rxn* rxn);
        void remove_rxn(Rxn* rxn);
        
        // ***************
        // MARK: - Geometry
        // ***************
        
        void add_geometry(Geometry *geometry);
        void remove_geometry(Geometry *geometry);
        
        // ***************
        // MARK: - ModelRxnIfce implementations
        // ***************
        
        void notify_fwd_rate_changed(Rxn* rxn, double fwd_rate);
        void notify_bkwd_rate_changed(Rxn* rxn, double bkwd_rate);

        // ***************
        // MARK: - ModelSpeciesIfce implementations
        // ***************
        
        void notify_diff_const_changed(Species* species, double diff_const);
    };
}
