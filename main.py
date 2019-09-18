from axelrod_py import *

N = 100
F = 10
q = 60

rand.seed(123457)

mysys = Axl_network(n = N, f = F, q = q, topology = 'random_regular', degree = 4)

mysys.evol2convergence()

print mysys.biggest_fragment()['size']

mysys.save_fragments_distribution('frag.dat')
