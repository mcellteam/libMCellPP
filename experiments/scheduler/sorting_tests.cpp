#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <forward_list>
#include <algorithm>
#include <map>
#include <cstdint>
#include <time.h>
#include <ctime>
#include <random>

using namespace std;


////////// Start of C version

struct abstract_element {
  struct abstract_element *next;
  double t; /* Time at which the element is scheduled */
};

/*************************************************************************
ae_list_sort:
  In: head of a linked list of abstract_elements
  Out: head of the newly sorted list
  Note: uses mergesort
*************************************************************************/

struct abstract_element *ae_list_sort(struct abstract_element *ae) {
  struct abstract_element *stack[64];
  int stack_n[64];
  struct abstract_element *left = NULL, *right = NULL, *merge = NULL, *tail = NULL;
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

////////// End of C version


////////// Start of C++ version

class SchedulableItem {
 public:
  SchedulableItem *next;
  double t;
  SchedulableItem ( double t ) {
    this->t = t;
  }
};

/*************************************************************************
ae_list_sort:
  In: head of a linked list of abstract_elements
  Out: head of the newly sorted list
  Note: uses mergesort
*************************************************************************/

SchedulableItem *ae_object_sort(SchedulableItem *ae) {
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

////////// End of C++ version

long num_vec_out_of_order ( vector<SchedulableItem *> ae_vec ) {
  auto num = ae_vec.size();
  auto i = num;
  long num_bad = 0;
  for (i=0; i<num-1; i++) {
    if ( ae_vec.at(i)->t > ae_vec.at(i+1)->t ) {
      num_bad += 1;
    }
  }
  return ( num_bad );
}


int main ( int argc, char *argv[] ) {

  cout.precision(15); // This is just enough to round 1.3899999999999999 to 1.39

  cout << "\n\n" << endl;
  cout << "*******************************" << endl;
  cout << "*   Sort Comparison C / C++   *" << endl;
  cout << "*******************************" << endl;
  cout << endl;

  double test_times[] = { 5.3, 0.1, 9.7, 8.2, 2.9, 2.8, 3.6 };
  int count = sizeof(test_times) / sizeof(double);

  struct abstract_element *ae=NULL, *ae_new=NULL, *ae_temp=NULL;

  for (int i=0; i<count; i++) {
    ae_new = (struct abstract_element *)calloc(1, sizeof(struct abstract_element));
    ae_new->t = test_times[(count-1)-i];
    ae_new->next = ae;
    ae = ae_new;
  }

  ///////////////////////////////

  cout << "Before Merge Struct sort:";
  ae_temp = ae;
  while (ae_temp != NULL) {
    cout << " " << ae_temp->t;
    ae_temp = ae_temp->next;
  }
  cout << endl;

  ae = ae_list_sort ( ae );

  cout << "After Merge Struct sort:";
  ae_temp = ae;
  while (ae_temp != NULL) {
    cout << " " << ae_temp->t;
    ae_temp = ae_temp->next;
  }
  cout << endl;  

  ///////////////////////////////

  vector<SchedulableItem *> ae_vec;

  for (int i=0; i<count; i++) {
    ae_vec.push_back ( new SchedulableItem(test_times[i]) );
  }

  ///////////////////////////////

  cout << "Before C++ Vector sort:";
  for (vector<SchedulableItem *>::iterator it=ae_vec.begin(); it!=ae_vec.end(); ++it) {
    cout << " " << (*it)->t;
  }
  cout << endl;  


  // Use a lambda function to return a boolean comparison result needed for sorting
  sort ( ae_vec.begin(), ae_vec.end(), [] (SchedulableItem *i, SchedulableItem *j) { return ( i->t < j->t ); } );


  cout << "After C++ Vector sort:";
  for (vector<SchedulableItem *>::iterator it=ae_vec.begin(); it!=ae_vec.end(); ++it) {
    cout << " " << (*it)->t;
  }
  cout << endl;


  ////// Time with large arrays

  long num_to_test = 2000000; // 14
  
  cout << endl << "Sorting " << num_to_test << " values ..." << endl << endl;

  forward_list<SchedulableItem *> ae_list;

  SchedulableItem *ae_item = NULL, *new_ae_item = NULL, *ae_item_temp = NULL;

  // Call these at definition time to benefit from auto typing.
  auto t_start = clock();
  auto t_stop = clock();

  unsigned seed;
  
  ae=NULL;
  ae_new=NULL;
  ae_vec.clear();

  seed = 872389273;
  mt19937 generator(seed);
  normal_distribution<double> distribution(0.0, 10.0);

  if (num_to_test < 20) {
    cout << "Unsorted Array:" << endl;
  }
  double rand_t;
  for (int i=0; i<num_to_test; i++) {
    rand_t = distribution(generator);
    if (num_to_test < 20) {
      cout << "  " << setprecision(5) << rand_t;
    }

    ae_new = (struct abstract_element *)calloc(1, sizeof(struct abstract_element));
    ae_new->t = rand_t;

    // Add new items to the front
    new_ae_item = new SchedulableItem(rand_t);
    new_ae_item->next = ae_item;
    ae_item = new_ae_item;

    ae_vec.push_back ( new SchedulableItem(rand_t) );
    ae_list.push_front ( new SchedulableItem(rand_t) );

    ae_new->next = ae;
    ae = ae_new;
  }
  if (num_to_test < 20) {
    cout << endl;
  }

  t_start = clock();
  ae = ae_list_sort ( ae );
  t_stop = clock();
  cout << "Elapsed time for Merge Struct Sorting: " << ((double)(t_stop-t_start))/CLOCKS_PER_SEC << " s\n";
  if (num_to_test < 20) {
    ae_temp = ae;
    while (ae_temp != NULL) {
      cout << "  " << setprecision(5) << ae_temp->t;
      ae_temp = ae_temp->next;
    }
    cout << endl;
  }

  t_start = clock();
  ae_item = ae_object_sort ( ae_item );
  t_stop = clock();
  cout << "Elapsed time for Merge Object Sorting: " << ((double)(t_stop-t_start))/CLOCKS_PER_SEC << " s\n";
  if (num_to_test < 20) {
    ae_item_temp = ae_item;
    while (ae_item_temp != NULL) {
      cout << "  " << setprecision(5) << ae_item_temp->t;
      ae_item_temp = ae_item_temp->next;
    }
    cout << endl;
  }

  cout << "Num out of order (before sorting) = " << num_vec_out_of_order ( ae_vec ) << endl;
  t_start = clock();
  sort ( ae_vec.begin(), ae_vec.end(), [] (SchedulableItem *i, SchedulableItem *j) { return ( i->t < j->t ); } );
  t_stop = clock();
  cout << "Num out of order (after sorting) = " << num_vec_out_of_order ( ae_vec ) << endl;
  if (num_to_test < 20) {
    auto num = ae_vec.size();
    auto i = num;
    for (i=0; i<num-1; i++) {
      cout << "  " << setprecision(5) << ae_vec.at(i)->t;
    }
    cout << endl;
  }
  cout << "Elapsed time for Vector Sorting: " << ((double)(t_stop-t_start))/CLOCKS_PER_SEC << " s\n";

  t_start = clock();
  ae_list.sort ( [] (SchedulableItem *i, SchedulableItem *j) { return ( i->t < j->t ); } );
  t_stop = clock();
  cout << "Elapsed time for List Sorting: " << ((double)(t_stop-t_start))/CLOCKS_PER_SEC << " s\n";



  ///////////////////////////////
  

  return ( 0 );
}


