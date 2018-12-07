# Local approximations to the MST (a question asked by Gabor)

Let T be a path of size n and assign a random point in [0,1]^2
to each vertex of T.  Now, select a random path abc in T of size 3
and, if |ab| > |ac| or |bc| > |ac| then replace the longer of those
two edges with the edge ac.  The process finishes when this is no longer
possible, so that, for every size 3 path abc, |ac| is the longest edge
of the triangle abc.

*Conclusion:* This algorithm does not produce very good trees.  It seems that
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
