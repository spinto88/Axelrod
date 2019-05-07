#include "evolution.h"

void evolution(axl_network *mysys)
{
	int i, j, k, r, neighbour;	
	int step_n;
        double h_ab, random;
	int n_active_links;
	active_link *active_links;

	/* Set the random seed */
	srand(mysys->seed);

	/* Look for active links */
	n_active_links = number_of_active_links(mysys);

	active_links = (active_link *)malloc(n_active_links * sizeof(active_link));

	k = 0;
	for(i = 0; i < mysys->nagents; i++)
	{
		for(j = 0; j < mysys->agent[i].degree; j++)
		{
			neighbour = mysys->agent[i].neighbors[j];
			if(active_condition(mysys->agent[i], mysys->agent[neighbour]))
			{
				active_links[k].source = i;
				active_links[k].target = neighbour;
				k++;
			}
		}
	}
	
	for(step_n = 0; step_n < n_active_links; step_n++)
	{
		/* Choose a random agent */
		k = rand() % n_active_links;

		i = active_links[k].source;
		j = active_links[k].target;

		/* Compute the homophily */
		h_ab = homophily(mysys->agent[i], mysys->agent[j]);
					   
		/* Take a random number */ 
    		random = (((double)rand())/RAND_MAX);

		/* If the interaction takes place, go into the next if */
	 	if((random < h_ab) && (active_condition(mysys->agent[i], mysys->agent[j])))
		{
			/* Take a random feature */
			r = rand() % mysys->agent[i].f;

			/* If the two agents share this feature, take the closest not equal */
			while(mysys->agent[i].feat[r] == mysys->agent[j].feat[r])
				r = (r+1) % mysys->agent[i].f;
      	    			        
			/* Agent i copies a feature from agent j */
			mysys->agent[i].feat[r] = mysys->agent[j].feat[r];
		}

		mysys->seed = rand();
	}
	free(active_links);

	return;
}
