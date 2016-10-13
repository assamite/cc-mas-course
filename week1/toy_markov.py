'''
.. py:module:: markov
    :platform: Unix

An example implementation of the first-order Markov Chain with toy data.
'''
import operator
import random

# We start by generating a toy distribution, setting a target length for our
# data set, and then generating the data set in a loop.

# This is our toy distribution of characters.
dist = 'Iä! Iä! Cthulhu for president!'

# Target length of the generated data
target = 10000

# Generate a data set with target length. Here, we loop 'len' times the
# for-loop and on each iteration draw random item from the 'dist'
data = ''.join([random.choice(dist) for _ in range(target)])

# For first-order Markov Chain, we have to iterate through the whole data set
# and keep count of the item pairs. We store these in a dictionary, where each
# key is an item (predecessor), and the value is another dictionary
# corresponding to the items following the predecessor, i.e. successors, and
# their counts.
pred_succ = {}
for i in range(len(data)-1):
    pred = data[i]
    succ = data[i+1]
    if pred not in pred_succ:
        # Predecessor key is not yet in the dictionary, so we create new
        # dictionary for it.
        pred_succ[pred] = {}

    if succ not in pred_succ[pred]:
        # Successor key is not yet in the dictionary, so we start counting from
        # one.
        pred_succ[pred][succ] = 1.0
    else:
        # Otherwise we just add one to the existing value.
        pred_succ[pred][succ] += 1.0

# Now that we have information of how many times each item is followed by
# any item, and that is all we need to create our Markov Chain. We start by 
# counting total number of successors for each item.
totals = {}
for pred, succ_counts in pred_succ.items():
    # Iterate over (key, value) -pairs of the outer dictionary (here value is 
    # another dictionary!) and sum inner dictionary's values for total number
    # of successors for item 'pred'.
    totals[pred] = sum(succ_counts.values())

# With total number of successors for each predecessor, we can compute the 
# probability for each successor given the predecessor.
probs = {}
for pred, succ_counts in pred_succ.items():
    probs[pred] = {}
    for succ, count in succ_counts.items():
        probs[pred][succ] = count / totals[pred]

# Next, we transform the data to a little more easily handled form for each
# predecessor, a cumulative distribution function (cdf) sorted from highest to
# lowest probability.
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

# Now, we can generate a Markov Chain the cdfs. We start by drawing a random 
# character from the distribution, and generate N characters overall.
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






