import networkx as nx
import warnings

def set_topology(G, topology, **kwargs):
 
    # Reset the graph
    for edge in G.edges():
        G.remove_edge(edge[0], edge[1])

    number_of_nodes = G.number_of_nodes()

    if topology == 'complete':
        """ 
	Complete graph.
	"""
        nx.complete_graph(number_of_nodes, G)

    elif topology == 'lattice':
	"""
	2D lattice with periodic bounded conditions
	"""
	side_nodes = number_of_nodes ** 0.5
	if int(side_nodes) != side_nodes:
	    warnings.warn('The number of agents must be a perfect square')
        else:
 	    aux_graph = nx.grid_2d_graph(int(side_nodes), int(side_nodes), periodic = True)
            A = nx.adjacency_matrix(aux_graph)
   	    nx.from_numpy_array(A.toarray(), create_using = G)

    elif topology == 'random_regular':
	"""
	Random regular network with mean degree
	"""
	aux_graph = nx.random_regular_graph(kwargs['degree'], number_of_nodes)

        A = nx.adjacency_matrix(aux_graph)
   	nx.from_numpy_array(A.toarray(), create_using = G)

    elif topology == 'cycle':
	"""
	Cycle network
	"""
   	nx.cycle_graph(number_of_nodes, create_using = G)
