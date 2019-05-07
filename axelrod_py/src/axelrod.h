#include <stdio.h>
#include <stdlib.h>

#ifndef AXL_AGENT
#define AXL_AGENT
/*
  Axelrod agent:
  An axelrod agent is caracterized by 
  a cultural vector with f components
  with represent the cultural features.
  Each feature can adopt q integer values,
  which represent the traits of a feature.
*/
struct _axl_agent
{
	int f; /* Number of features.*/
	int q; /* Number of traits per feature.*/
	int *feat; /*!< Cutural vector with f components.*/
	int degree; /* Node degree */
	int *neighbors; /* List of neighbors which are contact links */
	int label; /* Label useful for the fragment identifier */
};
typedef struct _axl_agent axl_agent; /*!< struct _axl_agent redefined as axl_agent. */
#endif

#ifndef AXL_NETWORK
#define AXL_NETWORK

/*
Axelrod network with n agents
*/
struct _axl_network
{
	int nagents; /* Number of axelrod agents in the network */
	axl_agent *agent; /* Vector of axelrod agents */
	int seed;
};
typedef struct _axl_network axl_network;
#endif
