// This is a C++ implementation of the MCell scheduler

/******************************************************************************
 *
 * Copyright (C) 2006-2015 by
 * The Salk Institute for Biological Studies and
 * Pittsburgh Supercomputing Center, Carnegie Mellon University
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
 * USA.
 *
******************************************************************************/

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <cstdint>

#include <string.h>
#include <float.h>

using namespace std;


/* Everything managed by scheduler must be derived from SchedulableItem */
class SchedulableItem {
 public:
  SchedulableItem *next=NULL; // nullptr ?
  double t;
  SchedulableItem () {
    this->t = 0;
  }
  SchedulableItem ( double t ) {
    this->t = t;
  }
  ~SchedulableItem() {
    // Should the destructor delete the list?
  }
  void delete_next_list () {
    SchedulableItem *one_after_next = NULL;
    while (next != NULL) {
      one_after_next = next->next;
      delete next;
      next = one_after_next;
    }
  }
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



/* Implements a multi-scale, discretized event scheduler */
class ScheduleWindow {  // Previously called a "struct schedule_helper"

 public:

  ScheduleWindow *next_scale=NULL;

  double dt=0;   // Timestep per slot in this particular scheduler
  double dt_1=0; // dt_1 = 1/dt
  double now=0;  // Start time of this scheduler

  /* Items scheduled now or after now */
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
    ScheduleWindow initialization:
      In: timestep per slot in this scheduler  ... is this correct?
          time for all slots in this scheduler ... is this correct?
          maximum number of slots in this scheduler
          the current time
  *************************************************************************/
  void init ( double dt_min, double dt_max, int maxlen, double start_iterations ) {

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
      this->next_scale = new ScheduleWindow ( dt_min * len, dt_max, maxlen, this->now + dt_min * len);
      this->next_scale->depth = this->depth + 1;
    }
  }

  /*************************************************************************
    ScheduleWindow full constructor:
      In: timestep per slot in this scheduler  ... is this correct?
          time for all slots in this scheduler ... is this correct?
          maximum number of slots in this scheduler
          the current time
  *************************************************************************/
  ScheduleWindow ( double dt_min, double dt_max, int maxlen, double start_iterations ) {
    init ( dt_min, dt_max, maxlen, start_iterations );
  }

  /*************************************************************************
    ScheduleWindow default constructor:
  *************************************************************************/
  ScheduleWindow () {
    init ( 1.0 * 5, 100.0, 5, 0.0 );
  }

  static int always_defunct (SchedulableItem *e) {
    return 1;
  }

  /*************************************************************************
    ScheduleWindow destructor:
  *************************************************************************/
  ~ScheduleWindow() {
    SchedulableItem *removed_items;
    removed_items = schedule_cleanup ( always_defunct );
    if (removed_items != NULL) {
      removed_items->delete_next_list();
      delete removed_items;
    }

    if (next_scale != NULL) {
      delete ( next_scale );
    }
    if (circ_buf_head != NULL) {
      for (int cbitem=0; cbitem<buf_len; cbitem++) {
        delete circ_buf_head[cbitem];
      }
      free ( circ_buf_head );
    }
    if (circ_buf_count != NULL) {
      free ( circ_buf_count );
    }
    if (current != NULL) {
      SchedulableItem *next_current;
      while (current != NULL) {
        next_current = current->next;
        delete current;
        current = next_current;
      }
    }
  }


/*******************************************************************************/
/*******************************************************************************/
/***************        sched_util.cpp starts here            ******************/
/*******************************************************************************/
/*******************************************************************************/


  /*************************************************************************
  item_list_sort:
    In: head of a linked list of SchedulableItem
    Out: head of the newly sorted list
    Note: uses mergesort
  *************************************************************************/

  SchedulableItem *item_list_sort(SchedulableItem *ae) {
    SchedulableItem *stack[64];
    int stack_n[64];
    SchedulableItem *left = NULL, *right = NULL, *merge = NULL, *tail = NULL;
    int si = 0;

    if (ae == NULL)
      return NULL;

    while (ae != NULL) {
      if (ae->next == NULL) {
        stack[si] = ae;
        stack_n[si] = 1;
        ae = NULL;
        si++;
      } else if (ae->t <= ae->next->t) {
        stack[si] = ae;
        stack_n[si] = 2;
        ae = ae->next->next;
        stack[si]->next->next = NULL;
        si++;
      } else {
        stack[si] = ae->next;
        stack_n[si] = 2;
        left = ae;
        ae = ae->next->next;
        stack[si]->next = left;
        left->next = NULL;
        si++;
      }
      while (si > 1 && stack_n[si - 1] * 2 >= stack_n[si - 2]) {
        stack_n[si - 2] += stack_n[si - 1];

        left = stack[si - 2];
        right = stack[si - 1];
        if (left->t <= right->t) {
          merge = left;
          left = left->next;
        } else {
          merge = right;
          right = right->next;
        }
        merge->next = NULL;
        tail = merge;

        while (1) {
          if (left == NULL) {
            tail->next = right;
            break;
          }
          if (right == NULL) {
            tail->next = left;
            break;
          }

          if (left->t <= right->t) {
            tail->next = left;
            tail = left;
            left = left->next;
          } else {
            tail->next = right;
            tail = right;
            right = right->next;
          }
        }

        stack[si - 2] = merge;
        si--;
      }
    }

    while (si > 1) /* Exact duplicate of code in loop--keep it this way! */
    {
      stack_n[si - 2] += stack_n[si - 1];

      left = stack[si - 2];
      right = stack[si - 1];
      if (left->t <= right->t) {
        merge = left;
        left = left->next;
      } else {
        merge = right;
        right = right->next;
      }
      merge->next = NULL;
      tail = merge;

      while (1) {
        if (left == NULL) {
          tail->next = right;
          break;
        }
        if (right == NULL) {
          tail->next = left;
          break;
        }

        if (left->t <= right->t) {
          tail->next = left;
          tail = left;
          left = left->next;
        } else {
          tail->next = right;
          tail = right;
          right = right->next;
        }
      }

      stack[si - 2] = merge;
      si--;
    }

    return stack[0];
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
      if (this->next_scale == NULL) {
        this->next_scale = new ScheduleWindow (
            this->dt * this->buf_len, this->dt * this->buf_len * this->buf_len, this->buf_len,
            this->now + this->dt * (this->buf_len - this->index));
        this->next_scale->depth = this->depth + 1;
      }

      /* insert item at coarser scale and insist that item is not placed in "current" list */
      return this->next_scale->insert_item(item, false);
    }

    return 0;
  }


  /*************************************************************************
  unlink_list_item:
    Removes a specific item from the linked list.

    In: SchedulableItem **hd - pointer to head of list
        SchedulableItem **tl - pointer to tail of list
        SchedulableItem *it - pointer to item to unlink
    Out: 0 on success, 1 if the item was not found
  *************************************************************************/
  static int unlink_list_item(SchedulableItem **hd,
                              SchedulableItem **tl,
                              SchedulableItem *it) {
    SchedulableItem *prev = NULL;

    while (*hd != NULL) {
      if (*hd == it) {
        (*hd) = (*hd)->next;
        if (*tl == it)
          *tl = prev;
        return 0;
      }

      prev = *hd;
      hd = &prev->next;
    }

    return 1;
  }


  /*************************************************************************
  schedule_deschedule:
    Removes an item from the schedule.

    In: struct schedule_helper *sh (now this) - the scheduler from which to remove
        SchedulableItem  *data - the item to remove
    Out: 0 on success, 1 if the item was not found
  *************************************************************************/
  int schedule_deschedule(SchedulableItem *ae) {
    // SchedulableItem *ae = (SchedulableItem *)data;

    /* If the item is in "current" */
    if (this->current && ae->t < this->now) {
      if (unlink_list_item(&this->current, &this->current_tail, ae))
        return 1;

      --this->current_count;
      return 0;
    }

    double nsteps = (ae->t - this->now) * this->dt_1;
    if (nsteps < ((double)this->buf_len)) {
      int list_idx;
      if (nsteps < 0.0)
        list_idx = this->index;
      else
        list_idx = (int)nsteps + this->index;
      if (list_idx >= this->buf_len)
        list_idx -= this->buf_len;

      if (unlink_list_item(&this->circ_buf_head[list_idx],
                           &this->circ_buf_tail[list_idx], ae)) {
        /* If we fail to find it in this level, it may be in the next level.
         * Note that when we are descheduling, we may need to look in more than
         * one place, depending upon how long ago the item to be descheduled was
         * originally scheduled. */
        if (this->next_scale) {
          if (!next_scale->schedule_deschedule(ae)) { // <-- Recursive call to schedule_deschedule
            --this->count;
            return 0;
          } else
            return 1;
        } else
          return 1;
      }

      --this->count;
      --this->circ_buf_count[list_idx];
      return 0;
    } else {
      if (!this->next_scale)
        return 1;

      if (!next_scale->schedule_deschedule(ae)) { // <-- Recursive call to schedule_deschedule
        --this->count;
        return 0;
      } else
        return 1;
    }
  }


  /*************************************************************************
  schedule_reschedule:
    Moves an item from one time to another in the schedule.

    In: struct schedule_helper *sh - the scheduler from which to remove
        SchedulableItem  *ae - the item to remove
        double new_t - the new time for the item
    Out: 0 on success, 1 if the item was not found
  *************************************************************************/
  int schedule_reschedule(SchedulableItem *ae, double new_t) {
    if (!schedule_deschedule(ae)) {
      ae->t = new_t;
      return insert_item(ae, 1);
    } else
      return 1;
  }


  /*************************************************************************
  schedule_advance:
    In: scheduler that we are using
        a pointer to the head-pointer for the list of the next time block
        a pointer to the tail-pointer for the list of the next time block
    Out: Number of items in the next block of time.  These items start
        with *head, and end with *tail.  Returns -1 on memory error.
  *************************************************************************/

  int schedule_advance(SchedulableItem **head, SchedulableItem **tail) {
    int n;
    SchedulableItem *p, *nextp;

    if (head != NULL)
      *head = this->circ_buf_head[this->index];
    if (tail != NULL)
      *tail = this->circ_buf_tail[this->index];

    this->circ_buf_head[this->index] = this->circ_buf_tail[this->index] = NULL;
    this->count -= n = this->circ_buf_count[this->index];
    this->circ_buf_count[this->index] = 0;

    this->index++;
    this->now += this->dt;

    if (this->index >= this->buf_len) {
      /* Move events from coarser time scale to this time scale */

      this->index = 0;
      if (this->next_scale != NULL) {
        /* Save our depth */
        int old_depth = this->depth;
        int conservecount = this->count;

        /* Hack: Toggle the non-zero-ness of our depth to toggle FIFO/LIFO
         * behavior
         */
        this->depth = old_depth ? 0 : -1;

        if (this->next_scale->schedule_advance(&p, NULL) == -1) {
          this->depth = old_depth;
          return -1;
        }
        while (p != NULL) {
          nextp = p->next;
          if (this->insert_item(p, 0)) {
            this->depth = old_depth;
            return -1;
          }
          p = nextp;
        }

        /* moved items were already counted when originally scheduled so don't
         * count again */
        this->count = conservecount;

        /* restore our depth */
        this->depth = old_depth;
      }
    }

    return n;
  }


  /*************************************************************************
  schedule_next:
    In: scheduler that we are using
    Out: Next item to deal with.  If we are out of items for the current
         timestep, NULL is returned and the time is advanced to the next
         timestep.  If there is a memory error, NULL is returned and
         sh->error is set to 1.
  *************************************************************************/

  SchedulableItem *schedule_next() {
    SchedulableItem *data;

    if (this->current == NULL) {
      this->current_count = schedule_advance(&this->current, &this->current_tail);
      if (this->current_count == -1)
        this->error = 1;
      return NULL;
    } else {
      this->current_count--;
      data = this->current;
      this->current = this->current->next;
      if (this->current == NULL)
        this->current_tail = NULL;
      return data;
    }
  }

  /*************************************************************************
  schedule_peak:
    In: scheduler that we are using
    Out: Next item (e.g. molecule) to deal with. NULL if scheduler is empty

    This is very similar to schedule_next, but the idea here is that we don't
    want to change the state of anything (specifically current_count).
    XXX: The caller needs to reset sh->current when it's done "peaking"

    // Note that this function is only used by "modify_rate_constant" in mcell_reactions.
    // It appears that modify_rate_constant saves and resets its current after "peaking" as advised.
  *************************************************************************/
  void *schedule_peak() {
    SchedulableItem *data;
    // Nothing to see here; move on
    if (this->current == NULL) {
      return NULL;
    }
    // Ooh. Found something!
    else {
      data = this->current;
      this->current = this->current->next;
      return data;
    }
  }


  /*************************************************************************
  schedule_anticipate:
    In: scheduler that we are using
        pointer to double to store the anticipated time of next event
    Out: 1 if there is an event anticipated, 0 otherwise
  *************************************************************************/

  int schedule_anticipate(double *t) {
    int i, j;
    double earliest_t = DBL_MAX;

    ScheduleWindow *sh = this;

    if (sh->current != NULL) {
      *t = sh->now;
      return 1;
    } else if (sh->count == 0)
      return 0;

    while (sh->next_scale != NULL && sh->count == sh->next_scale->count)
      sh = sh->next_scale;

    for (; sh != NULL; sh = sh->next_scale) {
      if (earliest_t < sh->now)
        break;

      for (i = 0; i < sh->buf_len; i++) {
        j = i + sh->index;
        if (j >= sh->buf_len)
          j -= sh->buf_len;
        if (sh->circ_buf_count[j] > 0) {
          earliest_t = sh->now + sh->dt * i;
          break;
        }
      }
    }

    if (earliest_t < DBL_MAX) {
      *t = earliest_t;
      return 1;
    } else
      return 0;
  }

  /*************************************************************************
  schedule_cleanup:
    In: scheduler that we are using
        pointer to a function that will return 0 if an abstract_element is
          okay, or 1 if it is defunct
    Out: all defunct items are removed from the scheduler and returned as
         a linked list (so appropriate action can be taken, such as
         deallocation)
  *************************************************************************/

  SchedulableItem * schedule_cleanup( int (*is_defunct)(SchedulableItem*), bool return_list=true) {

    ScheduleWindow *sh = this;

    SchedulableItem *defunct_list;
    SchedulableItem *ae;
    SchedulableItem *temp;
    ScheduleWindow *top;
    ScheduleWindow *shp;
    int i;

    defunct_list = NULL;

    top = sh;
    for (; sh != NULL; sh = sh->next_scale) {
      sh->defunct_count = 0;

      for (i = 0; i < sh->buf_len; i++) {
        /* Remove defunct elements from beginning of list */
        while (sh->circ_buf_head[i] != NULL &&
               (*is_defunct)(sh->circ_buf_head[i])) {
          temp = sh->circ_buf_head[i]->next;
          sh->circ_buf_head[i]->next = defunct_list;
          defunct_list = sh->circ_buf_head[i];
          sh->circ_buf_head[i] = temp;
          sh->circ_buf_count[i]--;
          sh->count--;
          for (shp = top; shp != sh; shp = shp->next_scale)
            shp->count--;
        }

        if (sh->circ_buf_head[i] == NULL) {
          sh->circ_buf_tail[i] = NULL;
        } else {
          /* Now remove defunct elements from later in list */
          for (ae = sh->circ_buf_head[i]; ae != NULL; ae = ae->next) {
            while (ae->next != NULL && (*is_defunct)(ae->next)) {
              temp = ae->next->next;
              ae->next->next = defunct_list;
              defunct_list = ae->next;
              ae->next = temp;
              sh->circ_buf_count[i]--;
              sh->count--;
              for (shp = top; shp != sh; shp = shp->next_scale)
                shp->count--;
            }
            if (ae->next == NULL) {
              sh->circ_buf_tail[i] = ae;
              break;
            }
          }
        }
      }
    }

    return defunct_list;
  }


  /*******************************************************************************/
  /*******************************************************************************/
  /*******************************************************************************/
  /*******************************************************************************/
  /*******************************************************************************/
  /*******************************************************************************/
  /***********                                                         ***********/
  /***********         Debug and Testing functions start here          ***********/
  /***********                                                         ***********/
  /*******************************************************************************/
  /*******************************************************************************/
  /*******************************************************************************/
  /*******************************************************************************/
  /*******************************************************************************/
  /*******************************************************************************/


  /*************************************************************************
    Indent the current output line by a specified amount
  *************************************************************************/
  void indent ( int depth ) {
    for (int i=0; i<depth; i++) { cout << "  "; }
  }

  /*************************************************************************
    Dump all the details of this schedule window and all following scales
  *************************************************************************/
  void full_dump ( int depth ) {
    indent(depth); cout << "ScheduleWindow at depth " << depth << ", current=" << (current!=NULL) << endl;
    indent(depth); cout << "  dt=" << dt << endl;
    indent(depth); cout << "  dt_1=" << dt_1 << endl;
    if (current == NULL) {
       indent(depth); cout << "  current is NULL" << endl;
    } else {
       indent(depth); cout << "  current = [ ";
       SchedulableItem *c;
       c = current;
       while (c != NULL) {
         printf ( "%g ", c->t );
         c = c->next;
       }
       printf ( "]\n" );
    }
    indent(depth); cout << "  now=" << now << endl;
    indent(depth); cout << "  count=" << count << " (total here and afterward)" << endl;
    indent(depth); cout << "  buf_len=" << buf_len << " (number of slots in this buffer)" << endl;
    indent(depth); cout << "  index=" << index << endl;

    int i;
    indent(depth); cout << "  count array (count in each bin): ";
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

    if (this->next_scale != NULL) {
      this->next_scale->full_dump(depth+1);
    }
  }

  /*************************************************************************
    Dump some of the details of this schedule window and all following scales
  *************************************************************************/
  void dump ( int depth ) {
    indent(depth); cout << "ScheduleWindow at depth " << depth << ", current=" << (current!=NULL) << ", dt=" << dt << ", now=" << now << ": [" << now << " " << now+(buf_len*dt) << ")" << endl;
    if (current == NULL) {
      indent(depth); cout << "  current i NULL" << endl;
    } else {
      indent(depth); cout << "  current = [ ";
      SchedulableItem *c;
      c = current;
      while (c != NULL) {
        cout << c->t << " ";
        c = c->next;
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

    if (this->next_scale != NULL) {
      this->next_scale->dump(depth+1);
    }
  }

  /*************************************************************************
    Print a list of the items in this schedule window and all following scales
  *************************************************************************/
  int list( int next_item_num ) {
    int i=0;
    for (i=0; i<1*(this->buf_len); i++) {   // Only dump the first half (second is duplicates)
      SchedulableItem *item;
      item = this->circ_buf_head[i];
      if (item != NULL) {
        do {
          cout << "  " << next_item_num << ": t = " << item->t << endl;
          next_item_num++;
          item = item->next;
        } while (item != NULL);
      }
    }

    if (this->next_scale != NULL) {
      i += this->next_scale->list(next_item_num);
    }
    return i;
  }


  /*************************************************************************
    Find the item at the requested position in the linked list of scales
  *************************************************************************/
  SchedulableItem * item_at ( int item_num, int start_num ) {
    int i=0;
    for (i=0; i<1*(this->buf_len); i++) {   // Only dump the first half (second is duplicates)
      SchedulableItem *item;
      item = this->circ_buf_head[i];
      if (item != NULL) {
        do {
          if (start_num == item_num) {
            cout << "    found " << start_num << ": t = " << item->t << endl;
            return ( item );
          }
          start_num++;
          item = item->next;
        } while (item != NULL);
      }
    }

    if (this->next_scale != NULL) {
       return this->next_scale->item_at(item_num, start_num);
    }
    return NULL;
  }


};



/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/
/***********                                                         ***********/
/***********              Validation code start here                 ***********/
/***********                                                         ***********/
/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/

SchedulableItem * new_element_at_time ( double t ) {
  SchedulableItem *ae = new SchedulableItem(t);
  ae->next = NULL;
  return ae;
}

SchedulableItem * insert_item_at_time ( ScheduleWindow *timestep_window, double t, int put_neg_in_current ) {
  SchedulableItem *ae = new SchedulableItem(t);
  ae->next = NULL;
  timestep_window->insert_item(ae, put_neg_in_current!=0);
  return ae;
}

ScheduleWindow *create_scheduler(double dt_min, double dt_max, int maxlen, double start_iterations) {
  ScheduleWindow *timestep_window = new ScheduleWindow ( dt_min, dt_max, maxlen, start_iterations );
  timestep_window->next_scale = NULL;
  return ( timestep_window );
}


#include <sys/time.h>

double elapsed(struct timeval *t1,struct timeval *t2)
{
  return 1000.0*(t2->tv_sec-t1->tv_sec) + 0.001*(t2->tv_usec-t1->tv_usec);
}

/*
int is_defunct_molecule(struct abstract_element *e) {
  return ((struct abstract_molecule *)e)->properties == NULL;
}
*/

int is_defunct_element (SchedulableItem *e) {
  return 1;
}


#define schedule_add(x, y) x->insert_item(y, 1);

int validate_main()
{
  int i,j;
  ScheduleWindow *sh = new ScheduleWindow();
  SchedulableItem ae[10],*aep;
  struct timeval tv[3];

  ae[0].t = 0.17;
  ae[1].t = 1231.9;
  ae[2].t = 2345119.43;
  ae[3].t = 85.5;
  ae[4].t = 0.151;
  ae[5].t = 2.415;
  ae[6].t = 16.15;
  ae[7].t = 2.1818;
  ae[8].t = 85.9;
  ae[9].t = 1958.2;

  sh = create_scheduler(1.0,7.0,7,0.0);

  schedule_add(sh,ae + 0);
  schedule_add(sh,ae + 1);
  schedule_add(sh,ae + 2);
  schedule_add(sh,ae + 3);
  schedule_add(sh,ae + 4);
  schedule_add(sh,ae + 5);
  schedule_add(sh,ae + 6);
  schedule_add(sh,ae + 7);
  schedule_add(sh,ae + 8);

  // Not available in current version:  schedule_excert(sh,ae+3,ae+9,sizeof(struct abstract_element));

  while (sh->count + sh->current_count > 0)
  {
/*
    debug_print_sh(sh);
    aep = schedule_next(sh);
    if (aep!=NULL) printf("Item scheduled at %f\n",aep->t);
*/
    i = sh->count + sh->current_count;
    while ((aep = sh->schedule_next()) != NULL)
    {
      printf("Item scheduled at %f (now=%f)\n",aep->t,sh->now);
      i--;
    }
    j=0;
    while (i>0 && (aep=sh->schedule_next())==NULL) j++;
    if (i>0 && j>0)
    {
      printf("Advanced %d timestep%s; ",j,(j==1)?"":"s");
      if (aep != NULL)
      {
        schedule_add(sh,aep);
        printf("added back @ %f.\n",aep->t);
      }
      else printf("WTF?\n");
    }

    printf("\n");
  }

  // sh->delete_scheduler(sh);
  delete sh;

  ae[0].t = 0.17;
  ae[1].t = 1231.9;
  ae[2].t = 2345119.43;
  ae[3].t = 85.5;
  ae[4].t = 0.151;
  ae[5].t = 2.415;
  ae[6].t = 16.15;
  ae[7].t = 2.1818;
  ae[8].t = 85.9;
  ae[9].t = 1958.2;

  sh = create_scheduler(1.5,9.0,7,0.0);

  printf("Scheduling: ");
  for (i=0;i<10;i++) printf("%.3f ",ae[i].t);
  printf("\n");

  schedule_add(sh,ae + 0);
  schedule_add(sh,ae + 1);
  schedule_add(sh,ae + 2);
  schedule_add(sh,ae + 3);
  schedule_add(sh,ae + 4);
  schedule_add(sh,ae + 5);
  schedule_add(sh,ae + 6);
  schedule_add(sh,ae + 7);
  schedule_add(sh,ae + 8);
  schedule_add(sh,ae + 9);

  printf("Scheduled with sorting: ");

  // Not available in current version:  schedule_sort(sh);
  while (sh->count + sh->current_count > 0)
  {
    i = sh->count + sh->current_count;
    while ((aep = sh->schedule_next()) != NULL) { printf("%.3f ",aep->t); i--; }
    j=0;
    while (i>0 && (aep=sh->schedule_next())==NULL) j++;
    if (i>0 && j>0)
    {
      if (aep != NULL)
      {
        schedule_add(sh,aep);
        // Not available in current version:  schedule_sort(sh);
      }
    }
  }
  printf("\n\n");

  printf("Sorting 10 items 1e6 times:\n");
  gettimeofday(&(tv[0]),NULL);
  for (i=0;i<1000000;i++)
  {
    for (j=0;j<9;j++) ae[j].next = &(ae[j+1]);
    ae[9].next = NULL;

    aep = sh->item_list_sort(&(ae[0]));
  }
  gettimeofday(&(tv[1]),NULL);
  printf("Took %.3f seconds.\n",elapsed(&(tv[0]),&(tv[1]))/1000.0);

  delete sh;

  cout << "\nWarning: Validate is known to cause memory leaks!!" << endl;
}



void create_test_case ( ScheduleWindow *timestep_window, int put_neg_in_current ) {

  SchedulableItem *item_00, *item_01, *item_02, *item_03;

  insert_item_at_time ( timestep_window, 0.0, put_neg_in_current );

  insert_item_at_time ( timestep_window, 0.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 0.1, put_neg_in_current );
  insert_item_at_time ( timestep_window, 0.3, put_neg_in_current );

  insert_item_at_time ( timestep_window, 0.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 0.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 0.1, put_neg_in_current );
  insert_item_at_time ( timestep_window, 0.3, put_neg_in_current );
  insert_item_at_time ( timestep_window, 0.3, put_neg_in_current );
  insert_item_at_time ( timestep_window, 0.9, put_neg_in_current );
  insert_item_at_time ( timestep_window, 1.3, put_neg_in_current );
  insert_item_at_time ( timestep_window, 1.5, put_neg_in_current );
  insert_item_at_time ( timestep_window, 1.7, put_neg_in_current );
  insert_item_at_time ( timestep_window, 2.1, put_neg_in_current );
  insert_item_at_time ( timestep_window, 2.9, put_neg_in_current );
  insert_item_at_time ( timestep_window, 2.7, put_neg_in_current );
  insert_item_at_time ( timestep_window, 2.0, put_neg_in_current );

  insert_item_at_time ( timestep_window, 3.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 3.5, put_neg_in_current );
  insert_item_at_time ( timestep_window, 3.9, put_neg_in_current );

  insert_item_at_time ( timestep_window, 4.9, put_neg_in_current );
  insert_item_at_time ( timestep_window, 4.99, put_neg_in_current );
  insert_item_at_time ( timestep_window, 4.999, put_neg_in_current );
  insert_item_at_time ( timestep_window, 5.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 5.1, put_neg_in_current );


  item_00 = insert_item_at_time ( timestep_window, 10.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 20.0, put_neg_in_current );

  timestep_window->schedule_reschedule(item_00, 30.0);

  timestep_window->insert_item ( item_01=new_element_at_time ( 29.0 ), put_neg_in_current );
  timestep_window->insert_item ( item_02=new_element_at_time ( 31.0 ), put_neg_in_current );
  timestep_window->insert_item ( item_03=new_element_at_time ( 40.0 ), put_neg_in_current );

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

  // dump ( timestep_window, 0 );

  timestep_window->schedule_deschedule(item_00);
  // Need to delete it after descheduling it!!!
  delete item_00;

  // dump ( timestep_window, 0 );

  timestep_window->schedule_deschedule(item_02);
  // Need to delete it after descheduling it!!!
  delete item_02;

  // dump ( timestep_window, 0 );

}


struct block_of_mem {
  struct block_of_mem *next;
  void *mem;
};

long long how_much_free() {
  long long amount_free = 0;
  try {
    long block_size = 1024 * 1024;
    bool ok;
    block_of_mem *block;
    block = (struct block_of_mem *) calloc ( sizeof(struct block_of_mem), 1 );
    if (block == NULL) {
      return ( 0L );
    }
    amount_free += sizeof(struct block_of_mem);
    block->next = NULL;
    block->mem = NULL;
    ok = true;
    do {
      // cout << "Try to allocate " << block_size << endl;
      void *mem = (void *) calloc ( block_size, 1 );
      if (mem == NULL) {
        if (block_size >= 2) {
          block_size = block_size / 2;
        } else {
          ok = false;
        }
      } else {
        amount_free += block_size;
        block_of_mem *new_block = (struct block_of_mem *) calloc ( sizeof(struct block_of_mem), 1 );
        if (new_block == NULL) {
          free ( mem );
          ok = false;
        } else {
          new_block->mem = mem;
          new_block->next = block;
          block = new_block;
          if (block_size < 1000000000L) {
            block_size = block_size * 2;
          }
        }
      }
    } while (ok);
    while (block != NULL) {
      // cout << "Free a block" << endl;
      free (block->mem);
      block_of_mem *next = block->next;
      free ( block );
      block = next;
    }
  } catch (exception e) {
  }
  return amount_free;
}



int main ( int argc, char *argv[] ) {

  cout << "\n\n" << endl;
  cout << "*******************************" << endl;
  cout << "*  Toy MCell Scheduler (C++)  *" << endl;
  cout << "*******************************" << endl;
  cout << endl;

  ScheduleWindow *timestep_window;

  cout << "Use \"h\" for help." << endl;


  double dt_min = 1.0;
  double dt_max = 100.0;
  int maxlen = 5;
  double start_iterations = 0;
  double test_time_offset = 0;
  int put_neg_in_current = 0;


  timestep_window = new ScheduleWindow (dt_min, dt_max, maxlen, start_iterations);

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
      printf ( "  S  = Sort current\n" );
      printf ( "  n  = Next (no dump)\n" );
      printf ( "  r# = Run n steps (no dump)\n" );
      printf ( "  -  = Toggle \"put negative in current\" flag\n" );
      printf ( "  w# = Window buffer width\n" );
      printf ( "  t  = Test case creation (fixed case)\n" );
      printf ( "  t# = Test case creation (distribution)\n" );
      printf ( "  T# = Time offset for insertion of test case events (adds an offset)\n" );
      printf ( "  V  = Validate using code from validate_sched_util.c\n" );
      printf ( "  m# = Move element # to a new time (prompted)\n" );
      printf ( "  x# = Remove element #\n" );
      printf ( "  F  = Report amount of free memory\n" );
      printf ( "  u  = Clean Up\n" );
      printf ( "  q  = Quit\n" );
    } else if (input[0] == 'c') {
      if (timestep_window != NULL) {
        printf ( "Deleting old scheduler\n" );
        delete timestep_window;
        timestep_window = NULL;
      }
      timestep_window = new ScheduleWindow (dt_min, dt_max, maxlen, start_iterations);
      printf ( "Created a new scheduler" );
    } else if (input[0] == 'i') {
      double t=0;
      sscanf ( &input[1], "%lg", &t );
      SchedulableItem *ae = new SchedulableItem(t);
      timestep_window->insert_item ( ae, put_neg_in_current );
      printf ( "Inserted item at time %lg", t );
    } else if (input[0] == 's') {
        SchedulableItem *ae = timestep_window->schedule_next();
        if (ae == NULL) {
          printf ( "No Event returned by schedule_next\n" );
        } else {
          printf ( "Handling event at t=%g\n", ae->t );
          delete ae;
        }
        timestep_window->dump ( 0 );
    } else if (input[0] == 'n') {
        SchedulableItem *ae = timestep_window->schedule_next();
        if (ae != NULL) {
          delete ae;
        }
    } else if (input[0] == 'r') {
      long n, i;
      sscanf ( &input[1], "%ld", &n );
      for (i=0; i<n; i++) {
        SchedulableItem *ae = timestep_window->schedule_next();
        if (ae == NULL) {
          // printf ( "No Event returned by schedule_next\n" );
        } else {
          printf ( "Handling event at t=%g\n", ae->t );
          delete ae;
        }
      }
    } else if (input[0] == 'd') {
        timestep_window->dump ( 0 );
    } else if (input[0] == 'l') {
        timestep_window->list (0);
    } else if (input[0] == 'f') {
        timestep_window->full_dump ( 0 );
    } else if (input[0] == 'V') {
        validate_main();
    } else if (input[0] == 't') {
        if (strlen(input) == 1) {
          create_test_case ( timestep_window, put_neg_in_current );
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
            SchedulableItem *ae = new SchedulableItem(test_time_offset+(norm*norm*num*num));
            timestep_window->insert_item ( ae, put_neg_in_current );
          }
        }
        // list ( timestep_window );
    } else if (input[0] == 'T') {
        if (strlen(input) == 0) {
          cout << "T option requires a time offset such as T3.5" << endl;
        } else {
          // Set the new start time
          double new_offset;
          sscanf ( &input[1], "%lg", &new_offset );
          cout << "Changing insertion start time from " << test_time_offset << " to " << new_offset << endl;
          test_time_offset = new_offset;
        }
    } else if (input[0] == 'w') {
      sscanf ( &input[1], "%d", &maxlen );
      printf ( "Window width will be %d for NEW schedulers", maxlen );

    } else if (input[0] == 'm') {
      int v_index;
      sscanf ( &input[1], "%d", &v_index );
      SchedulableItem *item = timestep_window->item_at(v_index,0);
      if ( item == NULL ) {
        cout << "Index " << v_index << " is invalid" << endl;
      } else {
        double new_time;
        cout << "Enter the new time for the item at " << item->t << " > ";
        cin >> new_time;
        cout << "Moving to time " << new_time << endl;
        timestep_window->schedule_reschedule(item, new_time);
      }
    } else if (input[0] == 'x') {
      int v_index;
      sscanf ( &input[1], "%d", &v_index );
      SchedulableItem *item = timestep_window->item_at(v_index,0);
      if ( item == NULL ) {
        cout << "Index " << v_index << " is invalid" << endl;
      } else {
        timestep_window->schedule_deschedule ( item );
        // Remember to delete it after descheduling it or it will cause a memory leak!!
        printf ( "Removed item at time %g.\n", item->t );
        delete item;
      }
    } else if (input[0] == 'u') {
      SchedulableItem *removed_items, *next_to_remove;
      removed_items = timestep_window->schedule_cleanup ( *is_defunct_element );
      if (removed_items != NULL) {
        removed_items->delete_next_list();
        delete removed_items;
      }
    } else if (input[0] == '-') {
        put_neg_in_current = !put_neg_in_current;
        printf ( "put_neg_in_current = %d\n", put_neg_in_current );
    } else if (input[0] == 'F') {
      static long long last_free = 0;
      static long long baseline = 0;
      try {
        long long free_now = how_much_free();
        if ( (baseline == 0) && (free_now == last_free) ) {
          baseline = free_now;
        }
        cout << "Amount free = " << free_now << " down " << baseline-free_now << endl;
        last_free = free_now;
      } catch (exception e) {
        cout << "Exception: " << endl;
      }
    } else if (input[0] == 'q') {
      delete timestep_window;
      cout << "Exiting..." << endl;
    } else {
      printf ( "Unknown command: %s", input );
    }
  } while ( strcmp(input,"q") != 0 );

  return ( 0 );
}

