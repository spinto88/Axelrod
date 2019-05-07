#ifndef ACTIVE_LINKS_H
#define ACTIVE_LINKS_H

#include "axelrod.h"
#include "homophily.h"

int active_condition(axl_agent, axl_agent);
int number_of_active_links(axl_network *);
int active_links(axl_network);

#endif
