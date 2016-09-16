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

#include "sched_util.h"


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

#include <sys/time.h>

double elapsed(struct timeval *t1,struct timeval *t2)
{
  return 1000.0*(t2->tv_sec-t1->tv_sec) + 0.001*(t2->tv_usec-t1->tv_usec);
}

void debug_print_sh(struct schedule_helper *sh)
{
  int i;
  struct abstract_element *aep;
  printf("dt %.2f, dt_1 %.2f, now %.2f, #%d/%d {",sh->dt,sh->dt_1,sh->now,sh->count,sh->current_count);
  aep = sh->current;
  if (aep!=NULL) printf(" ");
  while (aep!=NULL) { printf("%f ",aep->t); aep = aep->next; }
  printf("} [ ");
  for (i=0;i<sh->buf_len;i++)
  {
    printf("{");
    aep = sh->circ_buf_head[i];
    if (aep!=NULL) printf(" ");
    while (aep!=NULL) { printf("%f ",aep->t); aep = aep->next; }
    printf("} ");
  }
  printf("]\n");
  if (sh->next_scale != NULL)
  {
    printf(" -> ");
    debug_print_sh(sh->next_scale);
  }
}

int validate_main()
{
  int i,j;
  struct schedule_helper *sh;
  struct abstract_element ae[10],*aep;
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
    while ((aep = schedule_next(sh)) != NULL)
    {
      printf("Item scheduled at %f (now=%f)\n",aep->t,sh->now);
      i--;
    }
    j=0;
    while (i>0 && (aep=schedule_next(sh))==NULL) j++;
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

  delete_scheduler(sh);

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
    while ((aep = schedule_next(sh)) != NULL) { printf("%.3f ",aep->t); i--; }
    j=0;
    while (i>0 && (aep=schedule_next(sh))==NULL) j++;
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

    aep = ae_list_sort(&(ae[0]));
  }
  gettimeofday(&(tv[1]),NULL);
  printf("Took %.3f seconds.\n",elapsed(&(tv[0]),&(tv[1]))/1000.0);
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

  /*
  item_00 = insert_item_at_time ( timestep_window, 10.0, put_neg_in_current );
  insert_item_at_time ( timestep_window, 20.0, put_neg_in_current );

  schedule_reschedule(timestep_window, item_00, 30.0);

  schedule_insert ( timestep_window, item_01=(void *)(new_element_at_time ( 29.0 )), put_neg_in_current );
  schedule_insert ( timestep_window, item_02=(void *)(new_element_at_time ( 31.0 )), put_neg_in_current );
  schedule_insert ( timestep_window, item_03=(void *)(new_element_at_time ( 40.0 )), put_neg_in_current );
  */

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

  /*

  // dump ( timestep_window, 0 );

  schedule_deschedule(timestep_window, item_00);

  // dump ( timestep_window, 0 );

  schedule_deschedule(timestep_window, item_02);

  // dump ( timestep_window, 0 );

  */

}


struct block_of_mem {
  struct block_of_mem *next;
  void *mem;
};

unsigned long how_much_free() {
  double amount_free = 0;
  // try {
    double block_size = 1024 * 1024;
    int ok;
    struct block_of_mem *block;
    block = (struct block_of_mem *) malloc ( sizeof(struct block_of_mem) );
    if (block == NULL) {
      return ( 0L );
    }
    amount_free += sizeof(struct block_of_mem);
    block->next = NULL;
    block->mem = NULL;
    ok = 1;
    do {
      // printf ( "Try to allocate %ld\n", block_size );
      void *mem = (void *) malloc ( block_size );
      if (mem == NULL) {
        if (block_size >= 2) {
          block_size = block_size / 2;
        } else {
          ok = 0;
        }
      } else {
        amount_free += block_size;
        struct block_of_mem *new_block = (struct block_of_mem *) malloc ( sizeof(struct block_of_mem) );
        if (new_block == NULL) {
          free ( mem );
          ok = 0;
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
      struct block_of_mem *next = block->next;
      free ( block );
      block = next;
    }
  // } catch (exception e) {
  // }
  return amount_free;
}


int next_element_index = 0;
int element_list_length = 0;
struct abstract_element **element_list = NULL;
double *element_time_list = NULL;

void free_element_lists () {
  if (element_list != NULL) {
    free(element_list);
    element_list = NULL;
  }
  if (element_time_list != NULL) {
    free(element_time_list);
    element_time_list = NULL;
  }
  next_element_index = 0;
  element_list_length = 0;
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
  double test_time_offset = 0;
  int put_neg_in_current = 0;

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
      printf ( "  T# = Time offset for insertion of test case events (adds an offset)\n" );
      printf ( "  v  = Show all assigned values\n" );
      printf ( "  V  = Validate using code from validate_sched_util.c\n" );
      printf ( "  x# = Remove element #\n" );
      printf ( "  F  = Report amount of free memory\n" );
      printf ( "  u  = Clean Up\n" );
      printf ( "  q  = Quit\n" );
    } else if (input[0] == 'c') {
      if (timestep_window != NULL) {
        printf ( "Deleting old scheduler\n" );
        delete_scheduler ( timestep_window );
        timestep_window = NULL;
      }
      free_element_lists();
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
          // printf ( "No Event returned by schedule_next\n" );
        } else {
          printf ( "Handling event at t=%g\n", ae->t );
          free ( ae );
          ae = NULL;
        }
      }
    } else if (input[0] == 'd') {
        dump ( timestep_window, 0 );
    } else if (input[0] == 'l') {
        list ( timestep_window );
    } else if (input[0] == 'f') {
        full_dump ( timestep_window, 0 );
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
            // printf ( "gaussian = %lg\n", norm );
            insert_item_at_time ( timestep_window, test_time_offset+(norm*norm*num*num), put_neg_in_current );
          }
        }
        // list ( timestep_window );
    } else if (input[0] == 'T') {
        if (strlen(input) == 0) {
          printf ( "T option requires a time offset such as T3.5\n" );
        } else {
          // Set the new start time
          double new_offset;
          sscanf ( &input[1], "%lg", &new_offset );
          printf ( "Changing insertion start time from %g to %g\n", test_time_offset, new_offset );
          test_time_offset = new_offset;
        }
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
            free_element_lists();
          }
        }
      }
    } else if (input[0] == 'u') {
        struct abstract_element *removed_items, *next_to_remove;
        removed_items = schedule_cleanup ( timestep_window, *is_defunct_element );
        while (removed_items != NULL) {
          next_to_remove = removed_items->next;
          printf ( "   Removed item at: %g\n", removed_items->t );
          free ( removed_items );
          removed_items = next_to_remove;
        }
    } else if (input[0] == '-') {
        put_neg_in_current = !put_neg_in_current;
        printf ( "put_neg_in_current = %d\n", put_neg_in_current );
    } else if (input[0] == 'F') {
      static double last_free = 0;
      static double baseline = 0;
      // try {
        double free_now = how_much_free();
        if ( (baseline == 0) && (free_now == last_free) ) {
          baseline = free_now;
        }
        printf ( "Amount free = %.0f down %.0f\n", free_now, baseline-free_now );
        last_free = free_now;
      // } catch (exception e) {
      //   cout << "Exception: " << endl;
      // }
    } else if (input[0] == 'q') {
      delete_scheduler ( timestep_window );
      free_element_lists();
      printf ( "Exiting..." );
    } else {
      printf ( "Unknown command: %s", input );
    }
  } while ( strcmp(input,"q") != 0 );

  return ( 0 );
}
