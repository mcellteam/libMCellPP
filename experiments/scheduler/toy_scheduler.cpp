#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <cstdint>

#include <string.h>

using namespace std;

class SchedulableItem {
 public:
  SchedulableItem ( double t ) {
    this->t = t;
  }
  SchedulableItem *next;
  double t;
};

class ReleaseEvent : SchedulableItem {
  double release_time;
};

class ReleaseEventConstant : ReleaseEvent {
  int number_to_release;
};

class ReleaseEventGaussian : ReleaseEvent {
  double mean;
  double standard_deviation;
};

class ReleaseEventConcentration : ReleaseEvent {
  double concentration;
};

class ScheduleWindow {  // Previously called a "struct schedule_helper"
 public:
  ScheduleWindow *next_coarser_window=NULL;

  double dt=0;   // Timestep per slot in this particular scheduler
  double dt_1=0; // dt_1 = 1/dt
  double now=0;  // Start time of this scheduler
  int count=0;   // Total number of items scheduled now or after ... in this scheduler?
  int buf_len=0; // Number of slots in this scheduler
  int index=0;   // Index of next time block


  int *circ_buf_count=0; /* How many items are scheduled in each slot */
  // Array of linked lists of scheduled items for each slot
  SchedulableItem **circ_buf_head=0; 
  // Array of tails of the linked lists
  SchedulableItem **circ_buf_tail=0; 

  /* Items scheduled before now */
  /* These events must be serviced before simulation can advance to now */
  int current_count=0;                     /* Number of current items */
  SchedulableItem *current=0;      /* List of items scheduled now */
  SchedulableItem *current_tail=0; /* Tail of list of items */

  int defunct_count=0; /* Number of defunct items (set by user)*/
  int error=0;         /* Error code (1 - on error, 0 - no errors) */
  int depth=0;         /* "Tier" of scheduler in timescale hierarchy, 0-based */



  /*************************************************************************
    indent and dump display a text view of this scheduler
  *************************************************************************/
  void indent ( int depth ) {
    for (int i=0; i<depth; i++) { cout << "  "; }
  }
  void full_dump ( int depth ) {
    indent(depth); cout << "ScheduleWindow at depth " << depth << "current=" << (current!=NULL) << endl;
    indent(depth); cout << "  dt=" << dt << endl;
    indent(depth); cout << "  dt_1=" << dt_1 << endl;
    indent(depth); cout << "  now=" << now << endl;
    indent(depth); cout << "  count=" << count << endl;
    indent(depth); cout << "  buf_len=" << buf_len << endl;
    indent(depth); cout << "  index=" << index << endl;

    int i;
    indent(depth); cout << "  count array: ";
    for (i=0; i<this->buf_len; i++) {
      cout << " " << this->circ_buf_count[i];
    }
    cout << endl;
    indent(depth); cout << "  circ buffer: ";
    for (i=0; i<2*(this->buf_len); i++) {
      if (i == buf_len) printf ( " ### " );
      SchedulableItem *item;
      item = this->circ_buf_head[i];
      if (item == NULL) {
        cout << "[_]";
      } else {
        cout << "[ ";
        do {
          cout << item->t << " ";
          item = item->next;
        } while (item != NULL);
        cout << "]";
      }
    }
    cout << endl;

    if (this->next_coarser_window != NULL) {
      this->next_coarser_window->full_dump(depth+1);
    }
  }

  void dump ( int depth ) {
    indent(depth); cout << "ScheduleWindow at depth " << depth << "current=" << (current!=NULL) << ", dt=" << dt << ", now=" << now << ": [" << now << " " << now+(buf_len*dt) << ")" << endl;
    if (current == NULL) {
      indent(depth); cout << "  current i NULL" << endl;
    } else {
      indent(depth); cout << "  current = [";
      SchedulableItem *item;
      item = current;
      while (item != NULL) {
        cout << item->t << " ";
      }
      cout << "]" << endl;
    }
    indent(depth); cout << "  circ buffer: ";
    for (int i=0; i<1*(this->buf_len); i++) {
      SchedulableItem *item;
      item = this->circ_buf_head[i];
      if (item == NULL) {
        cout << "[_]";
      } else {
        cout << "[ ";
        do {
          cout << item->t << " ";
          item = item->next;
        } while (item != NULL);
        cout << "]";
      }
    }
    cout << endl;

    if (this->next_coarser_window != NULL) {
      this->next_coarser_window->dump(depth+1);
    }
  }

  void list() {
    int i;
    for (i=0; i<1*(this->buf_len); i++) {   // Only dump the first half (second is duplicates)
      SchedulableItem *item;
      item = this->circ_buf_head[i];
      if (item != NULL) {
        do {
          cout << "  t = " << item->t << endl;
          item = item->next;
        } while (item != NULL);
      }
    }

    if (this->next_coarser_window != NULL) {
      this->next_coarser_window->list();
    }
  }


  /*************************************************************************
    ScheduleWindow constructor:
      In: timestep per slot in this scheduler  ... is this correct?
          time for all slots in this scheduler ... is this correct?
          maximum number of slots in this scheduler
          the current time
  *************************************************************************/
  ScheduleWindow ( double dt_min, double dt_max, int maxlen, double start_iterations ) {

    double n_slots = dt_max / dt_min;
    int len;

    if (n_slots < (double)(maxlen - 1))
      len = (int)n_slots + 1;
    else
      len = maxlen;

    if (len < 2)
      len = 2;

    this->dt = dt_min;
    this->dt_1 = 1 / dt_min;

    this->now = start_iterations;
    this->buf_len = len;

    this->circ_buf_count = (int *)calloc(len, sizeof(int));

    this->circ_buf_head = (SchedulableItem **)calloc(len * 2, sizeof(SchedulableItem*));

    this->circ_buf_tail = this->circ_buf_head + len;

    if (this->dt * this->buf_len < dt_max) {
      this->next_coarser_window = new ScheduleWindow ( dt_min * len, dt_max, maxlen, this->now + dt_min * len);
      this->next_coarser_window->depth = this->depth + 1;
    }
  }

  ~ScheduleWindow() {
    cout << "!!!!!!!!!!!!!!!!!!!!!!!" << endl;
    cout << "!! Destructor called !!" << endl;
    cout << "!!!!!!!!!!!!!!!!!!!!!!!" << endl;
    cout << "!!    Memory Leak    !!" << endl;
    cout << "!!!!!!!!!!!!!!!!!!!!!!!" << endl;
  }

  /*************************************************************************
    insert_item:
    In: item to schedule
        flag to indicate whether times in the "past" go into the list
           of current events (if false, go into next event, not current).
    Out: 0 on success, not sure if errors should throw an exception
  *************************************************************************/
  int insert_item ( SchedulableItem *item, bool put_neg_in_current ) {

    if (put_neg_in_current && item->t < this->now) {
      /* insert item into current list */
      this->current_count++;
      if (this->current_tail == NULL) {
        this->current = this->current_tail = item;
        item->next = NULL;
      } else {
        this->current_tail->next = item;
        this->current_tail = item;
        item->next = NULL;
      }
      return 0;
    }

    /* insert item into future lists */
    this->count++;
    double nsteps = (item->t - this->now) * this->dt_1;

    if (nsteps < ((double)this->buf_len)) {
      /* item fits in array for this scale */
      int i;
      if (nsteps < 0.0)
        i = this->index;
      else
        i = (int)nsteps + this->index;
      if (i >= this->buf_len)
        i -= this->buf_len;

      if (this->circ_buf_tail[i] == NULL) {
        this->circ_buf_count[i] = 1;
        this->circ_buf_head[i] = this->circ_buf_tail[i] = item;
        item->next = NULL;
      } else {
        this->circ_buf_count[i]++;

        /* For schedulers other than the first tier, maintain a LIFO ordering */
        if (this->depth) {
          item->next = this->circ_buf_head[i];
          this->circ_buf_head[i] = item;
        }

        /* For first-tier scheduler, maintain FIFO ordering */
        else {
          this->circ_buf_tail[i]->next = item;
          item->next = NULL;
          this->circ_buf_tail[i] = item;
        }
      }
    } else {
      /* item fits in array for coarser scale */
      if (this->next_coarser_window == NULL) {
        this->next_coarser_window = new ScheduleWindow (
            this->dt * this->buf_len, this->dt * this->buf_len * this->buf_len, this->buf_len,
            this->now + this->dt * (this->buf_len - this->index));
        this->next_coarser_window->depth = this->depth + 1;
      }

      /* insert item at coarser scale and insist that item is not placed in "current" list */
      return this->next_coarser_window->insert_item(item, false);
    }

    return 0;
  }

};


// This function creates a compatible interface with the C version
//
// Normal C++:
//    timestep_window->insert_item ( new SchedulableItem(t), true );
//
// Normal C:
//    struct abstract_element *ae = (struct abstract_element *) malloc ( sizeof(struct abstract_element) );
//    ae->t = t;
//    schedule_insert(my_helper, (void *)ae, true);
//
void insert_item_at_time ( ScheduleWindow *timestep_window, double t, int put_neg_in_current ) {
  SchedulableItem *ae = new SchedulableItem(t);
  timestep_window->insert_item(ae, put_neg_in_current!=0);
}


// This function creates a compatible interface with the C version
ScheduleWindow *create_scheduler(double dt_min, double dt_max, int maxlen, double start_iterations) {
  ScheduleWindow *timestep_window = new ScheduleWindow ( dt_min, dt_max, maxlen, start_iterations );
  return ( timestep_window );
}




int main ( int argc, char *argv[] ) {

  cout << "\n\n" << endl;
  cout << "*******************************" << endl;
  cout << "*  Toy MCell Scheduler (C++)  *" << endl;
  cout << "*******************************" << endl;
  cout << endl;

  cout << "Make a new timestep_window" << endl;

  ScheduleWindow *timestep_window;

  cout << "Make a new timestep_window and insert items\n" << endl;

  printf ( "Use \"h\" for help.\n" );

  // The following code is the same in C or C++

  double dt_min = 1.0;
  double dt_max = 100.0;
  int maxlen = 5;
  double start_iterations = 0;
  int put_neg_in_current = 0;

  int next_element_index = 0;
  int element_list_length = 0;
  SchedulableItem **element_list = NULL;
  double *element_time_list = NULL;

  timestep_window = new ScheduleWindow (dt_min, dt_max, maxlen, start_iterations);

  timestep_window->insert_item ( new SchedulableItem(3.33), put_neg_in_current );

  insert_item_at_time ( timestep_window, 0.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 0.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 0.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 0.1, put_neg_in_current );
  insert_item_at_time ( timestep_window, 0.3, put_neg_in_current );
  insert_item_at_time ( timestep_window, 0.3, put_neg_in_current );
  insert_item_at_time ( timestep_window, 0.9, put_neg_in_current );
  insert_item_at_time ( timestep_window, 1.3, put_neg_in_current );
  insert_item_at_time ( timestep_window, 2.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 3.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 5.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 10.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 20.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 21.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 22.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 23.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 50.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 100.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 200.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 201.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 202.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 500.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 501.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 502.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 503.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 504.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 1000.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 2000.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 5000.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 10000.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 20000.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 50000.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 100000.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 200000.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 500000.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 1000000.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 2000000.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 5000000.0, put_neg_in_current );



  timestep_window->dump(0);


  char input[1000];
  do {
    printf ( "\n-> " );
    scanf ( "%s", input );
    if ((input[0] == 'h')||(input[0] == '?')) {
      printf ( "  h  = Help\n" );
      printf ( "  c  = Create a new scheduler (delete old if it exists)\n" );
      printf ( "  l  = List all times in scheduler\n" );
      printf ( "  d  = Dump scheduler internal structures\n" );
      printf ( "  f  = Full dump of scheduler internal structures\n" );
      printf ( "  i# = Insert at time t=# (no space between \"i\" and time)\n" );
      printf ( "  s  = Step and Dump\n" );
      printf ( "  n  = Next (no dump)\n" );
      printf ( "  r# = Run n steps (no dump)\n" );
      printf ( "  -  = Toggle \"put negative in current\" flag\n" );
      printf ( "  w# = Window buffer width\n" );
      printf ( "  t  = Test case creation (fixed case)\n" );
      printf ( "  t# = Test case creation (distribution)\n" );
      printf ( "  v  = Show all assigned values\n" );
      printf ( "  V  = Validate using code from validate_sched_util.c\n" );
      printf ( "  x# = Remove element #\n" );
      printf ( "  u  = Clean Up\n" );
      printf ( "  q  = Quit\n" );
    } else if (input[0] == 'c') {
      if (timestep_window != NULL) {
        printf ( "Deleting old scheduler\n" );
        delete timestep_window;
        // delete_scheduler ( timestep_window );
        timestep_window = NULL;
      }
      if (element_list != NULL) {
        free(element_list);
        element_list = NULL;
      }
      if (element_time_list != NULL) {
        free(element_time_list);
        element_time_list = NULL;
      }
      timestep_window = new ScheduleWindow (dt_min, dt_max, maxlen, start_iterations);
      next_element_index = 0;
      printf ( "Created a new scheduler" );
    } else if (input[0] == 'i') {
      double t;
      sscanf ( &input[1], "%lg", &t );

      // Do the actual insertion
      SchedulableItem *ae = new SchedulableItem(t);
      timestep_window->insert_item ( ae, put_neg_in_current );

      // Keep track of items by ID for deletion
      if (element_list == NULL) {
        element_list_length = 1;
        element_list = (SchedulableItem **) calloc ( element_list_length, sizeof(SchedulableItem *) );
        element_time_list = (double *) calloc ( element_list_length, sizeof(double) );
        int i;
        for (i=0; i<element_list_length; i++) {
          element_list[i] = NULL;
          element_time_list[i] = -1;
        }
        next_element_index = 0;
      }
      if (next_element_index >= element_list_length) {
        // printf ( "Expanding values list ...\n" );
        // Allocate new arrays
        int new_element_list_length = element_list_length*2;
        SchedulableItem **new_element_list = (SchedulableItem **) calloc ( new_element_list_length, sizeof(SchedulableItem *) );
        double *new_element_time_list = (double *) calloc ( new_element_list_length, sizeof(double) );
        // Copy data into new arrays
        int i;
        for (i=0; i<element_list_length; i++) {
          new_element_list[i] = element_list[i];
          new_element_time_list[i] = element_time_list[i];
        }
        for (i=element_list_length; i<new_element_list_length; i++) {
          new_element_list[i] = NULL;
          new_element_time_list[i] = -1;
        }
        // Free old arrays and assign new arrays to pointers
        free(element_list);
        element_list = new_element_list;
        free(element_time_list);
        element_time_list = new_element_time_list;
        element_list_length = new_element_list_length;
      }
      element_list[next_element_index] = ae;
      element_time_list[next_element_index] = t;

      printf ( "Inserted item #%d at time %lg", next_element_index, t );
      next_element_index += 1;
    } else if (input[0] == 'v') {
      if (element_list == NULL) {
        printf ( "No assigned value indexes" );
      } else {
        int i;
        for (i=0; i<next_element_index; i++) {
          //if (element_list[i]!=NULL) {
            printf ( "  index %d stores t=%g at %p\n", i, element_time_list[i], (void *)(element_list[i]) );
          //}
        }
      }

/* schedule_next not defined yet
    } else if (input[0] == 's') {
        struct abstract_element *ae = (struct abstract_element *) schedule_next ( timestep_window );
        if (ae == NULL) {
          printf ( "No Event returned by schedule_next\n" );
        } else {
          printf ( "Handling event at t=%g\n", ae->t );
        }
        dump ( timestep_window, 0 );
    } else if (input[0] == 'n') {
        struct abstract_element *ae = (struct abstract_element *) schedule_next ( timestep_window );
    } else if (input[0] == 'r') {
      long n, i;
      sscanf ( &input[1], "%ld", &n );
      for (i=0; i<n; i++) {
        struct abstract_element *ae = (struct abstract_element *) schedule_next ( timestep_window );
        if (ae == NULL) {
          printf ( "No Event returned by schedule_next\n" );
        } else {
          printf ( "Handling event at t=%g\n", ae->t );
        }
      }
*/
    } else if (input[0] == 'd') {
        timestep_window->dump ( 0 );
    } else if (input[0] == 'l') {
        timestep_window->list ();
    } else if (input[0] == 'f') {
        timestep_window->full_dump ( 0 );
/*
    } else if (input[0] == 'V') {
        validate_main();
*/
    } else if (input[0] == 't') {
        if (strlen(input) == 1) {
          // create_test_case ( timestep_window, put_neg_in_current );
        } else {
          // Generate test data
          double norm;
          int num;
          sscanf ( &input[1], "%d", &num );
          norm = num;
          int n;
          for (n=0; n<num; n++) {
            int i;
            norm = -6.0;
            for (i=0; i<12; i++) {
              norm += drand48();
            }
            SchedulableItem *ae = new SchedulableItem(norm*norm*num*num);
            timestep_window->insert_item ( ae, put_neg_in_current );
          }
        }
        // list ( timestep_window );
/*
    } else if (input[0] == 'w') {
      sscanf ( &input[1], "%d", &maxlen );
      printf ( "Window width will be %d for NEW schedulers", maxlen );
    } else if (input[0] == 'x') {
      int v_index;
      sscanf ( &input[1], "%d", &v_index );
      if ( (v_index<0) || (v_index>=next_element_index) ) {
        printf ( "Index %d is outside of range: 0 <= i <= %d\n", v_index, next_element_index-1 );
      } else {
        if (element_list[v_index] == NULL) {
          printf ( "Item %d is already deleted.", v_index );
        } else {
          schedule_deschedule ( timestep_window, (void *)(element_list[v_index]) );
          element_list[v_index] = NULL;
          printf ( "Removed item at time %g.\n", element_time_list[v_index] );
          element_time_list[v_index] = -1.0;
          int i;
          int empty = 1;
          for (i=0; i<next_element_index; i++) {
            if (element_time_list[i] >= 0) {
              empty = 0;
              break;
            }
          }
          if (empty==1) {
            printf ( "All value indexes are empty, so remove the arrays.\n" );
            if (element_list != NULL) {
              free(element_list);
              element_list = NULL;
            }
            if (element_time_list != NULL) {
              free(element_time_list);
              element_time_list = NULL;
            }
            next_element_index = 0;
          }
        }
      }
    } else if (input[0] == 'u') {
        struct abstract_element *removed_items, *next_removed;
        removed_items = schedule_cleanup ( timestep_window, *is_defunct_element );
        next_removed = removed_items;
        while (next_removed != NULL) {
          printf ( "   Removed item at: %g\n", next_removed->t );
          next_removed = next_removed->next;
        }
*/
    } else if (input[0] == '-') {
        put_neg_in_current = !put_neg_in_current;
        printf ( "put_neg_in_current = %d\n", put_neg_in_current );
    } else if (input[0] == 'q') {
      cout << "Exiting..." << endl;
    } else {
      printf ( "Unknown command: %s", input );
    }
  } while ( strcmp(input,"q") != 0 );

  return ( 0 );
}


