#!/usr/bin/python3
""" Small program for testing a conjecture/question about local algorithms
    for computing the MST of a random point set.

    Let T be a path of size n and assign a random point in [0,1]^2
    to each vertex of T.  Now, select a random path abc in T of size 3
    and, if |ab| > |ac| or |bc| > |ac| then replace the longer of those
    two edges with the edge ac.  The process finishes when this is no longer
    possible, so that, for every size 3 path abc, |ac| is the longest edge
    of the triangle abc.

    Conclusion: This algorithm does not produce very good trees.  It seems that
    the resulting spanning tree has total length approximately .38n whereas the
    MST has total length O(sqrt(n)).  Is there a simple rigorous proof that the
    resulting tree was total length Omega(n)?

    Two possible generalizations:

    1. Select two random vertices u and v of T whose distance is at most k and
       consider the path u=x_1,...,x_r=v in T.  Consider doing any improvement
       that involves removing somme edge x_ix_{i+1} and replacing it with the
       closest pair ab with a in {x_1,...,x_i} and b in {x_{i+1},...,x_r}.

    2. Select a random connected subtree T' of T of size k and replace the edges
       of T' with the MST of V(T').

    There is a reasonable probability that one or both of these algorithms
    produces a tree of expected length O(sqrt(n)) for a sufficiently large k.
    Maybe k >= c*log n is sufficient?

    The second algorithm obviously produces the MST if k=n.  Slightly less
    obviously, the first algorithm does also:  If uv is an edge of the MST 
    that it not already in T, then the path from u to v in T contains at least
    one edge of length greater than |uv|.
"""
import sys
import random
import itertools
import functools
import math




""" Make a path on the vertex set {0,...,n-1} """
def make_path(n):
    neighbours = [{i-1,i+1} for i in range(n)]
    neighbours[0].remove(-1)
    neighbours[-1].remove(n)
    return neighbours

""" Select a random path of length two """
def random_2path(neighbours):
    paths = [
        [(a[0],i,a[1]) for a in itertools.combinations(neighbours[i], 2)]
        for i in range(len(neighbours)) ]
    paths = list(itertools.chain.from_iterable(paths))
    return random.choice(paths)

""" Return a list of all slideable 2-paths """
def slideable_2paths(neighbours, points):
    paths = [
        [(a[0],i,a[1]) for a in itertools.combinations(neighbours[i], 2)]
        for i in range(len(neighbours)) ]
    paths = list(itertools.chain.from_iterable(paths))
    return [ p for p in paths if is_slideable([points[x] for x in p]) ]


""" Return the squared distance between points a and b """
def distance_sq(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

""" Return the distance between points a and b """
def distance(a, b):
    return math.sqrt(distance_sq(a,b))

""" Return the index i of the longest edge (i,i+1) in the cycle """
def longest_edge(cycle):
    d = [distance_sq(cycle[i], cycle[(i+1)%len(cycle)]) for i in range(len(cycle))]
    m = max(d)
    return d.index(m)

""" Return true iff replacing """
def is_slideable(cycle):
    return longest_edge(cycle) != len(cycle)-1

""" Replace the edge ij with the edge ik """
def slide_edge(neighbours, path):
    (i,j,k) = path
    neighbours[i].remove(j)
    neighbours[j].remove(i)
    neighbours[i].add(k)
    neighbours[k].add(i)

""" Compute the total (squared) lenght of the graph """
def total_length(neighbours, points):
    length = 0
    for i in range(len(neighbours)):
        for j in neighbours[i]:
            length += distance(points[i],points[j])
    return length

import matplotlib.pyplot as plt

def draw_graph(neighbours, points):
    for i in range(len(neighbours)):
        plt.plot([points[i][0]], [points[i][1]], "ro")
        for j in neighbours[i]:
            plt.plot((points[i][0], points[j][0]), (points[i][1], points[j][1]), "k")
    plt.show()

if __name__ == "__main__":
    n = 100
    if len(sys.argv) == 2:
        n = int(sys.argv[1])
    points = [(random.random(), random.random()) for _ in range(n)]
    neighbours = make_path(n)
    #print(points)
    #print(neighbours)
    print(total_length(neighbours, points))
    paths = slideable_2paths(neighbours, points)
#    paths = None
    print(neighbours)
    while paths:
        p = random.choice(paths)
        #print(p)
        t = [points[i] for i in p]
        j = longest_edge(t)
        #print(j)
        if j == 0:
            slide_edge(neighbours, (p[0], p[1], p[2]))
        else:
            slide_edge(neighbours, (p[2], p[1], p[0]))
        print(total_length(neighbours, points))
        paths = slideable_2paths(neighbours, points)
        #paths = None
    #print(neighbours)
    draw_graph(neighbours, points)
