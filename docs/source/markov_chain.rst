Markov Chains
==============

Markov chain (MC) is a stochastic process that satisfies the Markov property
(in some terms *memorylessness*). The Markov property means, that one can give
as good predictions about the system's future given the present state as one
could knowing the full history of the system.

When dealing with natural language, the state of a system is typically a
specified number of successive chunks of text (characters, words, etc.), called
*tokens*. For first-order Markov chains the state is one token (i.e. one word
or character) and for higher-order chains the states contain more tokens (two
for second-order, etc.).

To generate a Markov chain, we need to have the probability for each successor
state given the current state (so called state transition probabilities). In
some cases the transition probabilities can be handed in advance, but in the
typical case they are computed from a given data.

Examples involving Markov chains:

	- :doc:`First-order Markov chain using toy data <toy_markov>`
