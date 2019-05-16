#ifndef FRAGMENT_IDENTIFIER_H
#define FRAGMENT_IDENTIFIER_H

#include "axelrod.h"
#include "homophily.h"

void swap(int*, int*);
int non_zero_hom(axl_agent, axl_agent);
int is_neighbour(axl_network *, int, int);
void fragment_identifier(axl_network *);

#endif
