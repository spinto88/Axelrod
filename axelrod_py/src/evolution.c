#include "evolution.h"

void evolution(axl_network *mysys)
{
	int i, j, r, aux_int;	
	int step_n;
        double h_ab, random;

	/* Set the random seed */
	srand(mysys->seed);
	
	for(step_n = 0; step_n < mysys->nagents; step_n++)
	{
		/* Choose a random agent */
		i = rand() % mysys->nagents;

		/* Choose a random neighbour of i */
		aux_int = rand() % mysys->agent[i].degree;
       		j = mysys->agent[i].neighbors[aux_int];

		/* Compute the homophily */
		h_ab = homophily(mysys->agent[i], mysys->agent[j]);
					   
		/* Take a random number */ 
    		random = (((double)rand())/RAND_MAX);

		/* If the interaction takes place, go into the next if */
	 	if((random < h_ab) && (h_ab != 1.00))
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

	return;
}
