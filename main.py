from axelrod_py import *

N = 1024
F = 10
q = 20

rand.seed(123457)

mysys = Axl_network(n = N, f = F, q = q, topology = 'lattice')

mysys.evol2convergence()

print mysys.biggest_fragment()['size']

mysys.save_fragments_distribution('frag.dat')
