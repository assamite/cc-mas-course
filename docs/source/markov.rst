Markov Chains
=============

Markov chains is is a stochastic process that satisfies the Markov property (in
some terms *memorylessness*). The Markov property means, that one can give as
good predictions about the system's future given the present state as one could
knowing the full history of the system.

In our case, when dealing with natural language, the state of the system is
specified number of preceding chunks of text (characters, words, etc.). For
first-order Markov chains this is the direct predecessor chunk (i.e. one word
or character).

To generate a Markov chain, we need to have the probability for each successor
given the current state (so called state transition probabilities). In some
cases this can be handed in advance, but in most of the interesting cases, it
is computed from a given data.

Next, we will show with a toy example, how first-order Markov chains can be
generated using Python. We start by creating the state transition probabilities
for the artificial data, and then generate text using these probabilities.

Creating Markov Chains
----------------------

`(full code) <>`_

First, we need to generate some data. Let the 