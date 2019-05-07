
#ifndef EVOLUTION_H
#define EVOLUTION_H

#include "axelrod.h"
#include "homophily.h"
#include "active_links.h"

struct _active_link{
	int source;
	int target;
};
typedef struct _active_link active_link;

void evolution(axl_network *);

#endif
