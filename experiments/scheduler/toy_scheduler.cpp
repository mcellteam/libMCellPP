/* File : libMCell.h */

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <cstdint>

using namespace std;

class SchedulableItem; // Forward declaration needed?

class SchedulableItem {
 public:
  SchedulableItem ( double t ) {
    this->t = t;
  }
  SchedulableItem *next;
  double t;
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

  void indent ( int depth ) {
    for (int i=0; i<depth; i++) {
      cout << "  ";
    }
  }
  void dump ( int depth ) {
    indent(depth); cout << "ScheduleWindow at depth " << depth << endl;
    indent(depth); cout << "  dt=" << dt << endl;
    indent(depth); cout << "  dt_1=" << dt_1 << endl;
    indent(depth); cout << "  now=" << now << endl;
    indent(depth); cout << "  count=" << count << endl;
    indent(depth); cout << "  buf_len=" << buf_len << endl;
    indent(depth); cout << "  index=" << index << endl;

    int i;
    indent(depth); printf ( "  count array: " );
    for (i=0; i<this->buf_len; i++) {
      printf ( " %d", this->circ_buf_count[i] );
    }
    printf ( "\n" );
    indent(depth); printf ( "  circ buffer: " );
    for (i=0; i<2*(this->buf_len); i++) {
      SchedulableItem *item;
      item = this->circ_buf_head[i];
      if (item == NULL) {
        printf ( "[_]" );
      } else {
        printf ( "[ " );
        do {
          printf ( "%g ", item->t );
          item = item->next;
        } while (item != NULL);
        printf ( "]" );
      }
    }
    printf ( "\n" );

    if (this->next_coarser_window != NULL) {
      this->next_coarser_window->dump(depth+1);
    }
  }

  ScheduleWindow ( double dt_min, double dt_max, int maxlen, double start_iterations ) {

    // cout << "Top of ScheduleWindow constructor with " << dt_min << " " << dt_max << " " << maxlen << " " << start_iterations << endl;

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

    // cout << "Bottom of ScheduleWindow constructor" << endl;

  }


  int insert_item ( SchedulableItem *item, bool put_neg_in_current ) {

    // cout << "Top of insert_item" << endl;
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
      // cout << "Return from insert_item after putting negative in current" << endl;
      return 0;
    }

    /* insert item into future lists */
    this->count++;
    double nsteps = (item->t - this->now) * this->dt_1;

    if (nsteps < ((double)this->buf_len)) {
      /* item fits in array for this scale */
      // cout << "Put item in current time scale" << endl;

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
      // cout << "Put item in coarser time scale" << endl;

      if (this->next_coarser_window == NULL) {
        /*
        this->next_coarser_window = create_scheduler(
            this->dt * this->buf_len, this->dt * this->buf_len * this->buf_len, this->buf_len,
            this->now + this->dt * (this->buf_len - this->index));
        */
        this->next_coarser_window = new ScheduleWindow (
            this->dt * this->buf_len, this->dt * this->buf_len * this->buf_len, this->buf_len,
            this->now + this->dt * (this->buf_len - this->index));
        this->next_coarser_window->depth = this->depth + 1;
      }

      /* insert item at coarser scale and insist that item is not placed in
       * "current" list */
      // cout << "Return from insert_item after scheduling coarser" << endl;
      return this->next_coarser_window->insert_item(item, false);
    }

    // cout << "Return from insert_item at very end" << endl;
    return 0;
  }

};


// This function creates a compatible interface with the C version
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


  // The following code is the same in C or C++

  double dt_min = 1.0;
  double dt_max = 100.0;
  int maxlen = 5;
  double start_iterations = 0;
  int put_neg_in_current = 0;

  timestep_window = create_scheduler(dt_min, dt_max, maxlen, start_iterations);

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

  return ( 0 );
}


