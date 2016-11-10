Week 1 - Markov Chains, Parsing
===============================

.. centered::
	(Tue 1.11. 15.45) The first week's exercises are now in their final form.

|

	#. **RETURN** Familiarize yourself with `Markov chains
	   <https://en.wikipedia.org/wiki/Markov_chain>`_, and how they can be
	   created from the data. See :doc:`toy_markov` for an example of how to
	   create Markov chain from a set of toy data.

	   Given a string ``babacccabac``:

		a. What are the states for the first-order Markov chain?
		b. What are the states for the second-order Markov chain?
		c. Compute the state transition probabilities for the first-order
		   Markov chain.

	#. Create first-order Markov chain from the book *Alice's Adventures in
	   Wonderland* by Lewis Carroll. See :doc:`parsing_NLTK` for the text
	   parsing instructions. The transitions should be counted from the 
	   ``sanitized_sentences`` data structure by looping over its list of
	   tokenized sentences (which are lists also), i.e. the last token of each
	   sentence is not succeeded by any state.

	   For sanity checking, here are the five most probable state successors
	   for the state 'Alice'::

		[('.', 0.17751479289940827),
 		 ('was', 0.047337278106508875),
 		 ('and', 0.047337278106508875),
 		 ('in', 0.03550295857988166),
 		 ("'s", 0.03550295857988166)]

	   What are overall 5 the most probable state transitions? What about
	   100 the most probable state transitions? Why so?

	#. Create a function ``markov_chain(raw_text)``, which takes a piece of raw
	   text (``str``) and returns the state transition probabilities. The
	   function first splits the raw text into sentences, then each sentence
	   into tokens and then computes the state transition probabilities from
	   the tokenized sentences.

	#. **RETURN** Create a function ``sanitize(token_list)``, which takes as an argument
	   a list of text tokens and sanitizes the list by removing inappropriate
	   tokens. Use different sanitization method than in the example, and try to
	   make it more "intelligent". Justify your choices and state them clearly
	   in the function's documentation.

	#. Alter the function ``markov_chain`` to accept an optional boolean
	   argument ``sanitize`` which defaults to ``True``. If it is true, each
	   tokenized sentence is sanitized (with your ``sanitize``-function) before
	   the state transition probabilities are computed.

	#. **RETURN** Create a function ``generate(state_transition_probabilities, length=10, start=None)``,
	   which returns a piece of text generated from given state transition
	   probabilities. Specification:

		#. The piece of text should be at most ``length`` tokens long and
		   concatenated into a single string.

		#. The generation should end without an exception if a state that has
		   no successors is generated and return the already generated string
		   (including the state with no successor).

		#. If ``start`` is other than ``None``, the generation should be started
		   from that state. Otherwise the generation is started from a random
		   state.

		#. Handle the case where the state given by ``start`` is not in the
		   transition probabilities. (Most probably raise an exception.)


	#. **RETURN** Dan Ventura formulates several "steps" towards more computationally
	   creative systems in his article 'Mere generation: Essential barometer or
	   dated concept?'. Shortly, write your opinions in which category your
	   ``generate`` function from the last exercise falls. Also answer the
	   question: "How would you make it more creative?". 5-10 sentences should
	   be enough.

	#. **RETURN** Create a function ``likelihood(text, state_transitions_probabilities)`` 
	   that computes the (pseudo)likelihood of the text using the state
	   transition probabilities. If some of the tokens (or state transitions)
	   derived from ``text`` are not in ``state_transition_probabilities``,
	   the function raises an error. Otherwise it returns the computed 
	   (pseudo)likelihood. Justify your choices when computing the (pseudo)likelihood
	   and state them clearly in the function's docstring.