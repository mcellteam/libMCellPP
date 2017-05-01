#include <iostream>
#include <vector>
#include <forward_list>
#include <list>  // stl_list.h?
#include <map>   // stl_map.h?

using namespace std;

// Diffuse
// React
// Count
// Display
// Events

// class Simulation;

class Event {
  protected: double t;
  protected: Event *next;

  public: Event ( double t ) : t(t), next(NULL) {
    // this->t = t;  // A more explicit version of t(t) above
    // this->next = NULL;
  }
  public: ~Event() {}
  public: void insert ( Event *e ) {
    if (e->t < t) {
      // This event happens before the current event
      // This should never happen
      cout << "New event at " << e->t << " happens before this event" << endl;
      exit(1);
    } else if (next == NULL) {
      // This is the last event, so add it
      next = e;
    } else if (e->t < next->t) {
      // The event happens between this event and the next
      e->next = next;
      next = e;
    } else {
      next->insert ( e );
    }
  }
  public: Event *get_next() {
    return next;
  }
  public: void dump() {
    cout << "Event at t " << t << endl;
    if (next != NULL) {
      next->dump();
    }
  }
  public: virtual void callback() = 0;
};

class TimeStepEvent : public Event {
  private: double dt = -1, tx = -1;
  public: TimeStepEvent ( double t, double dt=-1, double tx=-1 ) : Event(t) {
    if (dt>=0) this->dt = dt;
    if (tx>=0) this->tx = tx;
  }
  public: virtual void callback() {
    cout << "TimeStepEvent callback at " << t << endl;
    if (dt >= 0) {
      // This is a repeating time step event
      if ( (tx < 0) || (t+dt<=tx) ) {
        insert ( new TimeStepEvent(t+dt,dt,tx) );
      }
    }
  }
};

class CountMolEvent : public Event {
  public: CountMolEvent ( double t ) : Event(t) { }
  public: virtual void callback() { cout << "CountMolEvent callback at " << t << endl; };
};

class StartSimEvent : public Event {
  public: StartSimEvent ( double t ) : Event(t) { }
  public: virtual void callback() { cout << "StartSimEvent callback at " << t << endl; };
};

class EndSimEvent : public Event {
  public: EndSimEvent ( double t ) : Event(t) { }
  public: virtual void callback() { cout << "EndSimEvent callback at " << t << endl; exit(0); };
};

class MolDecayEvent : public Event {
  public: MolDecayEvent ( double t ) : Event(t) { }
  public: virtual void callback() { cout << "MolDecayEvent callback at " << t << endl; };
};

class CollisionEvent : public Event {
  public: CollisionEvent ( double t ) : Event(t) { }
  public: virtual void callback();
};

class ReactionEvent : public CollisionEvent {
  public: ReactionEvent ( double t ) : CollisionEvent(t) { }
  public: virtual void callback() { cout << "ReactionEvent callback at " << t << endl; };
};

void CollisionEvent::callback() {
  cout << "CollisionEvent callback at " << t << endl;
  // Should do this randomly
  insert ( new ReactionEvent(t+0.0001) );
}

/*
class CallBack {
  public:
    virtual void callback ( Simulation sim ) = 0;
};
  
class Simulation {
  vector<CallBack> callback_list;
};
*/

int main() {
  Event *events;
  // Add events
  events = new StartSimEvent(0.0);
  events->insert(new EndSimEvent(10.0));
  events->insert(new TimeStepEvent(0.0,0.5));
  events->insert(new TimeStepEvent(5.0,0.01,5.1));
  events->insert(new TimeStepEvent(9.6,0.1));
  events->insert(new MolDecayEvent(0.1));
  events->insert(new CountMolEvent(2.1));
  events->insert(new ReactionEvent(5.5));
  events->insert(new TimeStepEvent(5.9));
  events->insert(new MolDecayEvent(2.2));
  events->insert(new CollisionEvent(2.4));
  events->dump();
  // Process events
  while (events != NULL) {
    events->callback();
    Event *temp;
    temp = events;
    events = events->get_next();
    delete temp;
  }
}

