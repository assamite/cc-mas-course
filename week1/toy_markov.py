'''
.. py:module:: markov
    :platform: Unix

An example implementation of the first-order Markov Chain with toy data.
'''
import operator
import random

# Generate some data
dist = 'Iä! Iä! Cthulhu for president!'
target = 10000
data = ''.join([random.choice(dist) for _ in range(target)])

# Count state transitions, i.e. predecessor-successor pairs.
transitions = {}
for i in range(len(data)-1):
    pred = data[i]
    succ = data[i+1]
    if pred not in transitions:
        # Predecessor key is not yet in the dictionary, so we create new
        # dictionary for it.
        transitions[pred] = {}

    if succ not in transitions[pred]:
        # Successor key is not yet in the dictionary, so we start counting from
        # one.
        transitions[pred][succ] = 1.0
    else:
        # Otherwise we just add one to the existing value.
        transitions[pred][succ] += 1.0

# Compute total number of successors for each state
totals = {}
for pred, succ_counts in transitions.items():
    totals[pred] = sum(succ_counts.values())

# Compute the probability for each successor given the predecessor.
probs = {}
for pred, succ_counts in transitions.items():
    probs[pred] = {}
    for succ, count in succ_counts.items():
        probs[pred][succ] = count / totals[pred]

# Transform the data to  a cumulative distribution function (cdf)
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
    cdf[-1][1] = 1.0 # We fix the last because of the possible rounding errors.
    cdfs[pred] = cdf
    print(pred, cdf)

# Generate text using cdfs
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






