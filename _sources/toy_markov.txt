Text Generation with First-Order Markov Chain
===========================================================

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

In the rest of this section we will show how a first-order Markov chain can be used as a
generative model. We start by creating the state transition probabilities for
an artificial dataset, and then generate text using these probabilities.

`(full code) <https://github.com/assamite/cc-mas-course/blob/master/week1/toy_markov.py>`_

Generate Data
-------------

First, we need to generate some data. For this example we will use a very simple
model, where we first define a distribution as a string of characters, and then
draw from that distribution the target number of items concatenating them
to another string. ::

	import random
	dist = 'Iä! Iä! Cthulhu for president!'
	target = 10000
	data = ''.join([random.choice(dist) for _ in range(target)])

Compute State Transition Probabilities
--------------------------------------

Next, our goal is to compute the state transition probabilities for the generated
data. In this example, each character in the generated string is a state and
subsequent pairs of characters represent state transitions. That is, a string
'abc' has two state transitions, from 'a' to 'b' and from 'b' to 'c'. (In
higher order Markov chains we would be interested in longer sequences of
characters, i.e. second-order Markov chain would have one state transition,
from 'ab' to 'bc'.)

State transition probabilities can be computed using nested dictionary as a
book-keeping data structure. The outer dictionary has the current (preceding)
state as a key, and the value of that key is another (inner) dictionary. The inner
dictionary has the succeeding states as keys and the values are the number of
times the succeeding state is observed after the preceding state. Populating
the data structure is straightforward, we go over the list of states one time,
and keep count of every predecessor-successor pair. ::

	transitions = {}
	for i in range(len(data)-1):
	    pred = data[i]
	    succ = data[i+1]
	    if pred not in transitions:
	        # Predecessor key is not yet in the outer dictionary, so we create
	        # a new dictionary for it.
	        transitions[pred] = {}

	    if succ not in transitions[pred]:
	        # Successor key is not yet in the inner dictionary, so we start
	        # counting from one.
	        transitions[pred][succ] = 1.0
	    else:
	        # Otherwise we just add one to the existing value.
	        transitions[pred][succ] += 1.0

Now we have information about how many times each state has directly been
succeeded by other states. (Right now, we do not care if our state transitions
are not complete in the sense that zero counts are not marked in the data
structure, in many cases it is be justified to add a small transition
probability between all states that have zero transitions.) Next, we will sum
up every state's total number of successors. ::

	totals = {}
	for pred, succ_counts in transitions.items():
		totals[pred] = sum(succ_counts.values())

Using ``totals``, we can compute the probabilities for each state transition
by dividing each successor's count for a state with the total number of
successors for that state::

	probs = {}
	for pred, succ_counts in transitions.items():
	    probs[pred] = {}
	    for succ, count in succ_counts.items():
	        probs[pred][succ] = count / totals[pred]

In theory, we now have the state transition probabilities which could be used
to generate text. However, before doing that, we will convert the data
structure to a more usable form by representing the probabilities with a
cumulative distribution function ordered from highest to lowest probability. ::

	import operator
	cdfs = {}
	for pred, succ_probs in probs.items():
	    items = succ_probs.items()
	    # Sort the list by the second index in each item and reverse it from
	    # highest to lowest.
	    sorted_items = sorted(items, key=operator.itemgetter(1), reverse=True)
	    cdf = []
	    cumulative_sum = 0.0
	    for c, prob in sorted_items:
	        cumulative_sum += prob
	        cdf.append([c, cumulative_sum])
	    cdf[-1][1] = 1.0 # For possible rounding errors
	    cdfs[pred] = cdf

Generate Text
-------------

Finally, all that is left is to generate some text using our ``cdfs`` data
structure. We start by drawing a random character from the distribution, and
generate *N* characters overall. Then we loop the generation loop until we have
generated enough items. In the generation loop, we will generate a random
number on each iteration and look from the cumulative distribution function of
``cdfs[state]`` the appropriate successive state. ::

	start = random.choice(dist)
	N = 10
	markov_chain = start

	while len(markov_chain) < N:
	    pred = markov_chain[-1] # Last element of the list
	    rnd = random.random() # Random number from 0 to 1
	    cdf = cdfs[pred]
	    cp = cdf[0][1]
	    i = 0
	    # Go through the cdf until the cumulative probability is higher than the
	    # random number 'rnd'.
	    while rnd > cp:
	    	i += 1
	    	cp = cdf[i][1]
	    succ = cdf[i][0]
	    #print(rnd, succ, cdf)
	    markov_chain += succ

	print(markov_chain)

That's it. We have now computed the state transition probabilities from a toy
data set, and used them to generate new data. It is quite easy to alter this
example to also generate higher-order Markov chains, but that is left for the
future work!
