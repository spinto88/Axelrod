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

    def __init__(self, n, f, q, topology = 'complete', noise = 0.00):
        
	"""
        Constructor: initializes the network.Graph first, and set the topology and the agents' states. 
	"""
        # Init graph properties
        nx.Graph.__init__(self)
        nx.empty_graph(n, self)
        self.nagents = n

        # Init agents' states
        self.init_agents(f, q)

        # Set noise rate or number of metric features
        self.noise = noise
 
        # Init topology
        self.set_topology(topology)

	# Random seed 
	self.seed = rand.randint(0, 10000)

    def set_topology(self, topology):
        """
        Set the network's topology
        """
        import set_topology as setop

        self.id_topology = topology

        setop.set_topology(self, topology)

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
        for i in range(0, n):
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
        if self.noise > 0.00:
            return "Convergence cannot be reached with noise in the system"

        steps = 0
    	while self.active_links() != 0:
            self.evolution(check_steps)
                
            steps += check_steps

	return steps

    def mean_homophily(self):

        homophilies = [self.agent[i].homophily(self.agent[j]) \
                       for i in range(self.nagents) for j in range(i+1, self.nagents)]

        return np.mean(homophilies)

    

    def image_opinion(self, fname = '', conf = ''):
        """
        This method prints on screen the matrix of first features, of course the system is a square lattice.
        It is not confident if q is larger than 63.
        If fname is different of the null string, the matrix is save in a file with that name. This one can be loaded by numpy.loadtxt(fname).
        """
        if self.id_topology < 3.2:

            import matplotlib.pyplot as plt

            N = self.nagents
            n = int(N ** 0.5)
            q_z = self.q_z
            matrix = []
            for i in range(0, n):
                row = []
                for j in range(0, n):
                    row.append(self.agent[(j + (i*n))].opinion)
                matrix.append(row)

            if fname != '':
                np.savetxt(fname + '.txt', matrix)

            plt.ion()
            figure = plt.figure(1)
            figure.clf()
            if(conf != ''):
                label = str(conf)
                ax = figure.add_subplot(111)
                ax.text(2, 6, label , bbox={'facecolor':'white', 'alpha':0.8, 'pad':10}, fontsize=15)
            plt.imshow(matrix, interpolation = 'nearest', vmin = 0, vmax = q_z)
            plt.colorbar()
            if fname != '':
                plt.savefig(fname + '.png', bbox_inches='tight')
            else:
                figure.canvas.draw()

        else:
            print "The system's network is not a square lattice"
            pass
    
        
    def image_vaccinated(self, fname = '', conf = ''):
        """
        This method prints on screen the matrix of vaccinated agents, of course the system is a square lattice.
        It is not confident if q is larger than 63.
        If fname is different of the null string, the matrix is save in a file with that name. This one can be loaded by numpy.loadtxt(fname).
        """
        if self.id_topology < 3.2:

            import matplotlib.pyplot as plt
            from matplotlib import colors

            N = self.nagents
            n = int(N ** 0.5)
            q_z = self.q_z
            matrix = []
            for i in range(0, n):
                row = []
                for j in range(0, n):
                    row.append(self.agent[(j + (i*n))].vaccine)
                matrix.append(row)

            if fname != '':
                np.savetxt(fname + '.txt', matrix)

            plt.ion()
            cmap = colors.ListedColormap(['red', 'green'])
            bounds=[0, 0.1, 1]
            norm = colors.BoundaryNorm(bounds, cmap.N)

            figure = plt.figure(2)
            figure.clf()
            if(conf != ''):
                label = str(conf)
                ax = figure.add_subplot(111)
                ax.text(2, 6, label , bbox={'facecolor':'white', 'alpha':0.8, 'pad':10}, fontsize=15)
            cmap = colors.ListedColormap(['red', 'green'])
            bounds=[0, 0.1, 1]

            plt.imshow(matrix, interpolation = 'nearest', cmap = cmap, norm = norm)

            plt.colorbar(cmap=cmap, norm=norm, boundaries=bounds, ticks=[0, 1])

            if fname != '':
                plt.savefig(fname + '.png', bbox_inches='tight')
            else:
                figure.canvas.draw()

        else:
            print "The system's network is not a square lattice"
            pass  
