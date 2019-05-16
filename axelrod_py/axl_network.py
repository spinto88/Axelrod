import os
import ctypes as C
import networkx as nx
import random as rand
import numpy as np
from axl_agent import *

libc = C.CDLL(os.getcwd() + '/axelrod_py/libc.so')

class Axl_network(nx.Graph, C.Structure):

    """
    Axelrod network: it has nagents axelrod agents, and an amount of noise in the dynamics of the system. This class inherites from the networkx.Graph the way to be described.
    """
    _fields_ = [('nagents', C.c_int),
                ('agent', C.POINTER(Axl_agent)),
		('seed', C.c_int)]

    def __init__(self, n, f, q, topology = 'complete', **kwargs):
        
	"""
        Constructor: initializes the network.Graph first, and set the topology and the agents' states. 
	"""
        # Init graph properties
        nx.Graph.__init__(self)
        nx.empty_graph(n, self)
        self.nagents = n

        # Model parameters
        self.f = f
        self.q = q

        # Init agents' states
        self.init_agents(f, q)
 
        # Init topology
        self.set_topology(topology, **kwargs)

	# Random seed 
	self.seed = rand.randint(0, 10000)

    def set_topology(self, topology, **kwargs):
        """
        Set the network's topology
        """
        import set_topology as setop

        self.id_topology = topology

        setop.set_topology(self, topology, **kwargs)

        for i in range(self.nagents):

            self.agent[i].degree = self.degree(i)
            self.agent[i].neighbors = (C.c_int * self.degree(i))(*self.neighbors(i))

    def init_agents(self, f, q):
        """
        Iniatialize the agents' state.
        """
        self.agent = (Axl_agent * self.nagents)()
    
        for i in range(self.nagents):
            self.agent[i] = Axl_agent(f, q)

    def evolution(self, steps = 1):
        """
	Make n steps asynchronius evolutions of the system
        """
        libc.evolution.argtypes = [C.POINTER(Axl_network)]

        for step in range(steps):
            libc.evolution(C.byref(self))


    def fragments(self):
        """
 	Fragment identifier: it returns the size of the biggest fragment, its state, 
	and the cluster distribution.
        It sees if the agents are neighbors and have the first feature less or equal
	than the clustering radio.
        """
       
        n = self.nagents
        libc.fragment_identifier.argtypes = [C.POINTER(Axl_network)]      

        libc.fragment_identifier(C.byref(self))

        # After this, the vector labels has the label of each agent
        from collections import defaultdict
        labels_size = defaultdict(int)
        for i in range(n):
            labels_size[self.agent[i].label] += 1
        
	return labels_size

    def biggest_fragment(self):

        labels_size = self.fragments()
        biggest = sorted(labels_size.items(), reverse = True, key = lambda x: x[1])[0]

        return {'size': biggest[1], 'label': biggest[0]}

    def active_links(self):

        """
	Active links: it returns True if there are active links in the system.
        """
	
	libc.active_links.argtypes = [Axl_network]
	libc.active_links.restype = C.c_int

	return libc.active_links(self)


    def evol2convergence(self, check_steps = 1000):
        """ 
	Evolution to convergence: the system evolves until there is no active links, checking this by check_steps. Noise must be equal to zero.
        """
        steps = 0
    	while self.active_links() != 0:
            self.evolution(check_steps)
                
            steps += check_steps

	return steps

    def mean_homophily(self):

        homophilies = [self.agent[i].homophily(self.agent[j]) \
                       for i in range(self.nagents) for j in range(i+1, self.nagents)]

        return np.mean(homophilies)

    def save_fragments_distribution(self, fname):

        fragment_sizes = [d[1] for d in self.fragments().items()]

        fp = open(fname, 'a')
        fp.write('{},{},'.format(self.f, self.q))
        fp.write(', '.join([str(s) for s in fragment_sizes]))
        fp.write('\n')
        fp.close()
