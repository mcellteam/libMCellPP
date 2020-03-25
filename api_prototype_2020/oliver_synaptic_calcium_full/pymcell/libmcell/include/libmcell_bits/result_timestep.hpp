//
//  result_timestep.hpp
//  libmcell
//
//  Created by Oliver Ernst on 2/23/20.
//

#ifndef result_timestep_hpp
#define result_timestep_hpp

#include <stdio.h>

#endif /* result_timestep_hpp */

namespace mcl {

class ResultTimestep {
    
private:
    
    // Success?
    bool _success;
    
    // Internal copy func/clean up
    void _clean_up();
    void _copy(const ResultTimestep& other);
    void _move(ResultTimestep &other);

public:
    
    // ***************
    // MARK: - Constructor
    // ***************
    
    ResultTimestep(bool success);
    ResultTimestep(const ResultTimestep& other);
    ResultTimestep& operator=(const ResultTimestep& other);
    ResultTimestep(ResultTimestep&& other);
    ResultTimestep& operator=(ResultTimestep&& other);
    ~ResultTimestep();
    
    // ***************
    // MARK: - Success
    // ***************
    
    bool get_success() const;
};

}
