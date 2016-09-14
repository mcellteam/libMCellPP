// This is intended to be the MCell scheduler with the following changes:
//   Additional comments have been added using "//" prefix
//   Additional debugging / user interface code has been added at the end

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

// #include "config.h"  /// Not used ... dynamically generated from config-nix.h?

#include <float.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

// #include "sched_util.h"

/****
  Scheduler functions:

  struct abstract_element*   ae_list_sort         (struct abstract_element *ae);
  struct schedule_helper*    create_scheduler     (double dt_min, double dt_max, int maxlen, double start_iterations);
  int                        schedule_insert      (struct schedule_helper *sh, void *data, int put_neg_in_current);
  int                        schedule_deschedule  (struct schedule_helper *sh, void *data);
  int                        schedule_reschedule  (struct schedule_helper *sh, void *data, double new_t);
  //void                     schedule_excert      (struct schedule_helper *sh,void *data,void *blank,int * size);
  int                        schedule_advance     (struct schedule_helper *sh, struct abstract_element **head,struct abstract_element **tail);
  void *                     schedule_next        (struct schedule_helper *sh);
  void *                     schedule_peak        (struct schedule_helper *sh);
  #define                    schedule_add         (x, y) schedule_insert((x), (y), 1)
  int                        schedule_anticipate  (struct schedule_helper *sh, double *t);
  struct abstract_element *  schedule_cleanup     (struct schedule_helper *sh, int (*is_defunct)(struct abstract_element *e));
  void                       delete_scheduler     (struct schedule_helper *sh);
****/



/*******************************************************************************/
/*******************************************************************************/
/***************         sched_util.h starts here             ******************/
/*******************************************************************************/
/*******************************************************************************/


/* Everything managed by scheduler must begin as if it were derived from
 * abstract_element */
struct abstract_element {
  struct abstract_element *next;
  double t; /* Time at which the element is scheduled */
};

/* Implements a multi-scale, discretized event scheduler */
struct schedule_helper {
  struct schedule_helper *next_scale; /* Next coarser time scale */

  double dt;   /* Timestep per slot */
  double dt_1; /* dt_1 = 1/dt */
  double now;  /* Start time of the scheduler */

  /* Items scheduled now or after now */
  int count;           /* Total number of items scheduled now or after */
  int buf_len;         /* Number of slots in the scheduler */
  int index;           /* Index of the next time block */
  int *circ_buf_count; /* How many items are scheduled in each slot */
  // Array of linked lists of scheduled items for each slot
  struct abstract_element **circ_buf_head; 
  // Array of tails of the linked lists
  struct abstract_element **circ_buf_tail; 

  /* Items scheduled before now */
  /* These events must be serviced before simulation can advance to now */
  int current_count;                     /* Number of current items */
  struct abstract_element *current;      /* List of items scheduled now */
  struct abstract_element *current_tail; /* Tail of list of items */

  int defunct_count; /* Number of defunct items (set by user)*/
  int error;         /* Error code (1 - on error, 0 - no errors) */
  int depth;         /* "Tier" of scheduler in timescale hierarchy, 0-based */
};

struct abstract_element *ae_list_sort(struct abstract_element *ae);

struct schedule_helper *create_scheduler(double dt_min, double dt_max,
                                         int maxlen, double start_iterations);

int schedule_insert(struct schedule_helper *sh, void *data, int put_neg_in_current);
int schedule_deschedule(struct schedule_helper *sh, void *data);
int schedule_reschedule(struct schedule_helper *sh, void *data, double new_t);
/*void schedule_excert(struct schedule_helper *sh,void *data,void *blank,int
 * size);*/
int schedule_advance(struct schedule_helper *sh, struct abstract_element **head,
                     struct abstract_element **tail);

void *schedule_next(struct schedule_helper *sh);
void *schedule_peak(struct schedule_helper *sh);
#define schedule_add(x, y) schedule_insert((x), (y), 1)

int schedule_anticipate(struct schedule_helper *sh, double *t);
struct abstract_element *schedule_cleanup(struct schedule_helper *sh,
                 int (*is_defunct)(struct abstract_element *e));

void delete_scheduler(struct schedule_helper *sh);



/*******************************************************************************/
/*******************************************************************************/
/***************         sched_util.c starts here             ******************/
/*******************************************************************************/
/*******************************************************************************/


/*************************************************************************
ae_list_sort:
  In: head of a linked list of abstract_elements
  Out: head of the newly sorted list
  Note: uses mergesort
*************************************************************************/

struct abstract_element *ae_list_sort(struct abstract_element *ae) {
  struct abstract_element *stack[64];
  int stack_n[64];
  struct abstract_element *left = NULL, *right = NULL, *merge = NULL,
                          *tail = NULL;
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
create_scheduler:
  In: timestep per slot in this scheduler
      time for all slots in this scheduler
      maximum number of slots in this scheduler
      the current time
  Out: pointer to a new instance of schedule_helper; pass this to later
       functions.  (Dispose of with delete_scheduler.)  Returns NULL
       if out of memory.
*************************************************************************/

struct schedule_helper *create_scheduler(double dt_min, double dt_max,
                                         int maxlen, double start_iterations) {
  double n_slots = dt_max / dt_min;
  int len;

  if (n_slots < (double)(maxlen - 1))
    len = (int)n_slots + 1;
  else
    len = maxlen;

  if (len < 2)
    len = 2;

  struct schedule_helper *sh = NULL;
  sh = (struct schedule_helper *)malloc(sizeof(struct schedule_helper));
  if (sh == NULL)
    return NULL;
  memset(sh, 0, sizeof(struct schedule_helper));

  sh->dt = dt_min;
  sh->dt_1 = 1 / dt_min;

  sh->now = start_iterations;
  sh->buf_len = len;

  sh->circ_buf_count = (int *)calloc(len, sizeof(int));  // calloc ( num_members, size_of_member )
  if (sh->circ_buf_count == NULL)
    goto failure;

  sh->circ_buf_head = (struct abstract_element **)calloc(
      len * 2, sizeof(struct abstract_element*));           // Why 2 times len? Is this to allow the "tail" to be past the actual data?
  if (sh->circ_buf_head == NULL)
    goto failure;
  sh->circ_buf_tail = sh->circ_buf_head + len;              // This puts the tail beyond the normal buffer data but in the additional (2xlen) elements.

  if (sh->dt * sh->buf_len < dt_max) {
    sh->next_scale =
        create_scheduler(dt_min * len, dt_max, maxlen, sh->now + dt_min * len);
    if (sh->next_scale == NULL)
      goto failure;
    sh->next_scale->depth = sh->depth + 1;
  }

  return sh;

failure:
  if (sh != NULL)
    delete_scheduler(sh);
  return NULL;
}

/*************************************************************************
schedule_insert:
  In: scheduler that we are using
      data to schedule (assumed to start with abstract_element struct)
      flag to indicate whether times in the "past" go into the list
         of current events (if 0, go into next event, not current).
  Out: 0 on success, 1 on memory allocation failure.  Data item is
       placed in scheduler at end of list for its time slot.
*************************************************************************/

int schedule_insert(struct schedule_helper *sh, void *data, int put_neg_in_current) {
  struct abstract_element *ae = (struct abstract_element *)data;

  if (put_neg_in_current && ae->t < sh->now) {
    /* insert item into current list */

    sh->current_count++;
    if (sh->current_tail == NULL) {
      sh->current = sh->current_tail = ae;
      ae->next = NULL;
    } else {
      sh->current_tail->next = ae;
      sh->current_tail = ae;
      ae->next = NULL;
    }
    return 0;
  }

  /* insert item into future lists */
  sh->count++;
  double nsteps = (ae->t - sh->now) * sh->dt_1;

  if (nsteps < ((double)sh->buf_len)) {
    /* item fits in array for this scale */

    int i;
    if (nsteps < 0.0)
      i = sh->index;
    else
      i = (int)nsteps + sh->index;
    if (i >= sh->buf_len)
      i -= sh->buf_len;    // This wraps the pointer as if by "mod"

    if (sh->circ_buf_tail[i] == NULL) {
      sh->circ_buf_count[i] = 1;
      sh->circ_buf_head[i] = sh->circ_buf_tail[i] = ae;
      ae->next = NULL;
    } else {
      sh->circ_buf_count[i]++;

      /* For schedulers other than the first tier, maintain a LIFO ordering */
      if (sh->depth) {
        ae->next = sh->circ_buf_head[i];
        sh->circ_buf_head[i] = ae;
      }

      /* For first-tier scheduler, maintain FIFO ordering */
      else {
        sh->circ_buf_tail[i]->next = ae;
        ae->next = NULL;
        sh->circ_buf_tail[i] = ae;
      }
    }
  } else {
    /* item fits in array for coarser scale */

    if (sh->next_scale == NULL) {
      sh->next_scale = create_scheduler(
          sh->dt * sh->buf_len, sh->dt * sh->buf_len * sh->buf_len, sh->buf_len,
          sh->now + sh->dt * (sh->buf_len - sh->index));
      if (sh->next_scale == NULL)
        return 1;
      sh->next_scale->depth = sh->depth + 1;
    }

    /* insert item at coarser scale and insist that item is not placed in
     * "current" list */
    return schedule_insert(sh->next_scale, data, 0);        // Recursive call to schedule_insert
  }

  return 0;
}

/*************************************************************************
unlink_list_item:
  Removes a specific item from the linked list.

  In: struct abstract_element **hd - pointer to head of list
      struct abstract_element **tl - pointer to tail of list
      struct abstract_element *it - pointer to item to unlink
  Out: 0 on success, 1 if the item was not found
*************************************************************************/
static int unlink_list_item(struct abstract_element **hd,
                            struct abstract_element **tl,
                            struct abstract_element *it) {
  struct abstract_element *prev = NULL;

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

  In: struct schedule_helper *sh - the scheduler from which to remove
      void  *data - the item to remove
  Out: 0 on success, 1 if the item was not found
*************************************************************************/
int schedule_deschedule(struct schedule_helper *sh, void *data) {
  struct abstract_element *ae = (struct abstract_element *)data;

  /* If the item is in "current" */
  if (sh->current && ae->t < sh->now) {
    if (unlink_list_item(&sh->current, &sh->current_tail, ae))
      return 1;

    --sh->current_count;
    return 0;
  }

  double nsteps = (ae->t - sh->now) * sh->dt_1;
  if (nsteps < ((double)sh->buf_len)) {
    int list_idx;
    if (nsteps < 0.0)
      list_idx = sh->index;
    else
      list_idx = (int)nsteps + sh->index;
    if (list_idx >= sh->buf_len)
      list_idx -= sh->buf_len;

    if (unlink_list_item(&sh->circ_buf_head[list_idx],
                         &sh->circ_buf_tail[list_idx], ae)) {
      /* If we fail to find it in this level, it may be in the next level.
       * Note that when we are descheduling, we may need to look in more than
       * one place, depending upon how long ago the item to be descheduled was
       * originally scheduled. */
      if (sh->next_scale) {
        if (!schedule_deschedule(sh->next_scale, data)) {
          --sh->count;
          return 0;
        } else
          return 1;
      } else
        return 1;
    }

    --sh->count;
    --sh->circ_buf_count[list_idx];
    return 0;
  } else {
    if (!sh->next_scale)
      return 1;

    if (!schedule_deschedule(sh->next_scale, data)) { /* <-- Recursive call to schedule_deschedule */
      --sh->count;
      return 0;
    } else
      return 1;
  }
}

/*************************************************************************
schedule_reschedule:
  Moves an item from one time to another in the schedule.

  In: struct schedule_helper *sh - the scheduler from which to remove
      void  *data - the item to remove
      double new_t - the new time for the item
  Out: 0 on success, 1 if the item was not found
*************************************************************************/
int schedule_reschedule(struct schedule_helper *sh, void *data, double new_t) {
  if (!schedule_deschedule(sh, data)) {
    struct abstract_element *ae = (struct abstract_element *)data;
    ae->t = new_t;
    return schedule_insert(sh, data, 1);
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

int schedule_advance(struct schedule_helper *sh, struct abstract_element **head,
                     struct abstract_element **tail) {
  int n;
  struct abstract_element *p, *nextp;

  if (head != NULL)
    *head = sh->circ_buf_head[sh->index];
  if (tail != NULL)
    *tail = sh->circ_buf_tail[sh->index];

  sh->circ_buf_head[sh->index] = sh->circ_buf_tail[sh->index] = NULL;
  sh->count -= n = sh->circ_buf_count[sh->index];
  sh->circ_buf_count[sh->index] = 0;

  sh->index++;
  sh->now += sh->dt;

  if (sh->index >= sh->buf_len) {
    /* Move events from coarser time scale to this time scale */

    sh->index = 0;
    if (sh->next_scale != NULL) {
      /* Save our depth */
      int old_depth = sh->depth;
      int conservecount = sh->count;

      /* Hack: Toggle the non-zero-ness of our depth to toggle FIFO/LIFO
       * behavior
       */
      sh->depth = old_depth ? 0 : -1;

      if (schedule_advance(sh->next_scale, &p, NULL) == -1) {
        sh->depth = old_depth;
        return -1;
      }
      while (p != NULL) {
        nextp = p->next;
        if (schedule_insert(sh, (void *)p, 0)) {
          sh->depth = old_depth;
          return -1;
        }
        p = nextp;
      }

      /* moved items were already counted when originally scheduled so don't
       * count again */
      sh->count = conservecount;

      /* restore our depth */
      sh->depth = old_depth;
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

void *schedule_next(struct schedule_helper *sh) {
  void *data;

  if (sh->current == NULL) {
    sh->current_count = schedule_advance(sh, &sh->current, &sh->current_tail);
    if (sh->current_count == -1)
      sh->error = 1;
    return NULL;
  } else {
    sh->current_count--;
    data = sh->current;
    sh->current = sh->current->next;
    if (sh->current == NULL)
      sh->current_tail = NULL;
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
void *schedule_peak(struct schedule_helper *sh) {
  void *data;
  // Nothing to see here; move on
  if (sh->current == NULL) {
    return NULL; 
  }
  // Ooh. Found something!
  else {
    data = sh->current;
    sh->current = sh->current->next;
    return data;
  }
}


/*************************************************************************
schedule_anticipate:
  In: scheduler that we are using
      pointer to double to store the anticipated time of next event
  Out: 1 if there is an event anticipated, 0 otherwise
*************************************************************************/

int schedule_anticipate(struct schedule_helper *sh, double *t) {
  int i, j;
  double earliest_t = DBL_MAX;

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

struct abstract_element *
schedule_cleanup(struct schedule_helper *sh,
                 int (*is_defunct)(struct abstract_element*)) {
  struct abstract_element *defunct_list;
  struct abstract_element *ae;
  struct abstract_element *temp;
  struct schedule_helper *top;
  struct schedule_helper *shp;
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

/*************************************************************************
delete_scheduler:
  In: scheduler that we are using
  Out: No return value.  The scheduler is freed from dynamic memory.
*************************************************************************/

void delete_scheduler(struct schedule_helper *sh) {
  if (sh) {
    if (sh->next_scale != NULL)
      delete_scheduler(sh->next_scale);
    if (sh->circ_buf_head)
      free(sh->circ_buf_head);
    if (sh->circ_buf_count)
      free(sh->circ_buf_count);
    free(sh);
  }
}




/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/
/***********                                                         ***********/
/***********            Testing functions start here                 ***********/
/***********                                                         ***********/
/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/
/*******************************************************************************/


/*
int is_defunct_molecule(struct abstract_element *e) {
  return ((struct abstract_molecule *)e)->properties == NULL;
}
*/

int is_defunct_element (struct abstract_element *e) {
  return 1;
}


struct abstract_element * new_element_at_time ( double t ) {
  struct abstract_element *ae = (struct abstract_element *) malloc ( sizeof(struct abstract_element) );
  ae->t = t;
  ae->next = NULL;
  return ae;
}

struct abstract_element * insert_item_at_time ( struct schedule_helper *my_helper, double t, int put_neg_in_current ) {
  struct abstract_element *ae = new_element_at_time ( t );
  schedule_insert(my_helper, (void *)ae, put_neg_in_current);
  return ae;
}


void indent ( int depth ) {
  int i;
  for (i=0; i<depth; i++) {
    printf ( "  " );
  }
}

void full_dump ( struct schedule_helper *helper, int depth ) {
  indent(depth); printf ( "ScheduleWindow at depth %d, current=%d\n", depth, helper->current != NULL );
  indent(depth); printf ( "  dt=%g\n", helper->dt );
  indent(depth); printf ( "  dt_1=%g\n", helper->dt_1 );
  if (helper->current == NULL) {
     indent(depth); printf ( "  current is NULL\n" );
  } else {
     indent(depth); printf ( "  current = [ " );
     struct abstract_element *c;
     c = helper->current;
     while (c != NULL) {
       printf ( "%g ", c->t );
       c = c->next;
     }
     printf ( "]\n" );
  }
  indent(depth); printf ( "  now=%g\n", helper->now );
  indent(depth); printf ( "  count=%d (total here and afterward)\n", helper->count );
  indent(depth); printf ( "  buf_len=%d (number of slots in this buffer)\n", helper->buf_len );
  indent(depth); printf ( "  index=%d\n", helper->index );

  int i;
  indent(depth); printf ( "  count array (count in each bin): " );
  for (i=0; i<helper->buf_len; i++) {
    printf ( " %d", helper->circ_buf_count[i] );
  }
  printf ( "\n" );
  indent(depth); printf ( "  circ buffer: " );
  for (i=0; i<2*(helper->buf_len); i++) {
    if (i == helper->buf_len) printf ( " ### " );
    struct abstract_element *item;
    item = helper->circ_buf_head[i];
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

  if (helper->next_scale != NULL) {
    full_dump ( helper->next_scale, depth+1 );
  }
}

void dump ( struct schedule_helper *helper, int depth ) {
  indent(depth); printf ( "ScheduleWindow at depth %d, current=%d, dt=%g, now=%g: [%g %g)\n", depth, helper->current != NULL, helper->dt, helper->now, helper->now, helper->now+(helper->buf_len*helper->dt) );
  int i;
  if (helper->current == NULL) {
     indent(depth); printf ( "  current is NULL\n" );
  } else {
     indent(depth); printf ( "  current = [ " );
     struct abstract_element *c;
     c = helper->current;
     while (c != NULL) {
       printf ( "%g ", c->t );
       c = c->next;
     }
     printf ( "]\n" );
  }
  indent(depth); printf ( "  circ buffer: " );
  for (i=0; i<1*(helper->buf_len); i++) {   // Only dump the first half (second is duplicates)
    struct abstract_element *item;
    item = helper->circ_buf_head[i];
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

  if (helper->next_scale != NULL) {
    dump ( helper->next_scale, depth+1 );
  }
}


void list ( struct schedule_helper *helper ) {
  int i;
  for (i=0; i<1*(helper->buf_len); i++) {   // Only dump the first half (second is duplicates)
    struct abstract_element *item;
    item = helper->circ_buf_head[i];
    if (item != NULL) {
      do {
        printf ( "  t = %g\n", item->t );
        item = item->next;
      } while (item != NULL);
    }
  }

  if (helper->next_scale != NULL) {
    list ( helper->next_scale );
  }
}

void create_test_case (  struct schedule_helper *timestep_window, int put_neg_in_current ) {

  struct abstract_element *item_00, *item_01, *item_02, *item_03;

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

  schedule_reschedule(timestep_window, item_00, 30.0);

  schedule_insert ( timestep_window, item_01=(void *)(new_element_at_time ( 29.0 )), put_neg_in_current );
  schedule_insert ( timestep_window, item_02=(void *)(new_element_at_time ( 31.0 )), put_neg_in_current );
  schedule_insert ( timestep_window, item_03=(void *)(new_element_at_time ( 40.0 )), put_neg_in_current );


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

  schedule_deschedule(timestep_window, item_00);

  // dump ( timestep_window, 0 );

  schedule_deschedule(timestep_window, item_02);

  // dump ( timestep_window, 0 );
}



int main ( int argc, char *argv[] ) {

  printf( "\n\n" );
  printf( "*****************************\n" );
  printf( "*  Toy MCell Scheduler (C)  *\n" );
  printf( "*****************************\n" );
  printf( "\n" );

  // struct abstract_element *ae;
  struct schedule_helper *timestep_window = NULL;

  printf ( "Use \"h\" for help.\n" );


  double dt_min = 1.0;
  double dt_max = 100.0;
  int maxlen = 5;
  double start_iterations = 0;
  int put_neg_in_current = 0;

  int next_element_index = 0;
  int element_list_length = 0;
  struct abstract_element **element_list = NULL;
  double *element_time_list = NULL;

  timestep_window = create_scheduler(dt_min, dt_max, maxlen, start_iterations);

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
      printf ( "  x# = Remove element #\n" );
      printf ( "  u  = Clean Up\n" );
      printf ( "  q  = Quit\n" );
    } else if (input[0] == 'c') {
      if (timestep_window != NULL) {
        printf ( "Deleting old scheduler\n" );
        delete_scheduler ( timestep_window );
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
      timestep_window = create_scheduler(dt_min, dt_max, maxlen, start_iterations);
      next_element_index = 0;
      printf ( "Created a new scheduler" );
    } else if (input[0] == 'i') {
      double t;
      sscanf ( &input[1], "%lg", &t );

      // Do the actual insertion
      struct abstract_element *ae = new_element_at_time ( t );
      schedule_insert(timestep_window, (void *)ae, put_neg_in_current);

      // Keep track of items by ID for deletion
      if (element_list == NULL) {
        element_list_length = 1;
        element_list = (struct abstract_element **) calloc ( element_list_length, sizeof(struct abstract_element *) );
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
        struct abstract_element **new_element_list = (struct abstract_element **) calloc ( new_element_list_length, sizeof(struct abstract_element *) );
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
    } else if (input[0] == 'd') {
        dump ( timestep_window, 0 );
    } else if (input[0] == 'l') {
        list ( timestep_window );
    } else if (input[0] == 'f') {
        full_dump ( timestep_window, 0 );
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
            // printf ( "gaussian = %lg\n", norm );
            insert_item_at_time ( timestep_window, norm*norm*num*num, put_neg_in_current );
          }
        }
        // list ( timestep_window );
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
    } else if (input[0] == '-') {
        put_neg_in_current = !put_neg_in_current;
        printf ( "put_neg_in_current = %d\n", put_neg_in_current );
    } else if (input[0] == 'q') {
      printf ( "Exiting..." );
    } else {
      printf ( "Unknown command: %s", input );
    }
  } while ( strcmp(input,"q") != 0 );

  return ( 0 );
}
