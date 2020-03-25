# API prototype

* `my_model.py` - creates a simple model.
* `main_simple.py` - simple example of running the model in a for loop.
* `main_advanced.py` and `main_parallel.py` - more complicated examples.

Note that they don't work.... yet....

There is also a test of the subscriber/observer + aggregation pattern in `subscriber_observer_pattern`:
* `subscriber_observer_pattern/test.py` - runs a simple test. **Note: this actually runs!**
* `subscriber_observer_pattern/pymcell` - contains the examples
  * `subscriber_observer_pattern/pymcell/rxn.py` - the reaction class
  * `subscriber_observer_pattern/pymcell/model.py` - the model class
  * `subscriber_observer_pattern/pymcell/model_part.py` - the subscriber/observer base class. Rxn is one of these.
  * `subscriber_observer_pattern/pymcell/model_rxn_ifce.py` - the interface to the model class that the reaction needs to know about.
