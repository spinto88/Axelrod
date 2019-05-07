#include "active_links.h"

int active_links(axl_network mysys)
{
	/* Active links: this function return if an active link is found.
	An active link is a pair of agents which are neighbors and the homophily
        is larger than zero and less than one. */

	int i, j;
        int n = mysys.nagents;
        int neighbor;
        double hab;

        for(i = 0; i < n; i++)
	{
		for(j = 0; j < mysys.agent[i].degree; j++)
		{
                        neighbor = mysys.agent[i].neighbors[j];

			hab = homophily(mysys.agent[i], mysys.agent[neighbor]);

			if((hab > 0.00) && (hab < 1.00))
				return 1;
		}
	}

	return 0;	
}
		

