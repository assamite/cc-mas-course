Exercises
=========

Weekly programming and other practical exercises for the course.

Preliminaries
-------------

	#. Set the development environment (see :doc:`setup`)

		- Install Python 3.5
		- Create a virtual environment
		- Install ``requirements.txt``

	#. Get used to Python (see :doc:`learn_python`)

		- Learn basic syntax. Things to consider include: loops, lists, 
		  dictionaries, ``def``, ``class``, ``import``, etc.

Week 1 - Markov Chains, Parsing
-------------------------------

	#. Familiarize yourself with Markov chains, and how they can be created
	   from the data. (see :doc:`toy_markov`)

	#. Create first-order Markov chain from the book *Alice's Adventures in
	   Wonderland* by Lewis Carroll (see :doc:`parsing_NLTK`).
	   The transitions should be counted from the splitted sentences, i.e. the
	   last token of each sentence is not succeeded by any state.

		#. What are the overall 5 most probable state transitions?
		#. What are the 5 most probable state successors for the state 'Alice'?

	#. Create a function ``markov_chain(raw_text)``, which splits the raw text
	   into sentences, the sentences into tokens, and returns the
	   state transition probabilities.

	#. Create a function ``sanitize(token_list)``, which takes as an argument
	   a list of text tokens and sanitizes the list by removing inappropriate
	   tokens.

	#. Alter the function ``markov_chain`` to accept an optional boolean
	   argument ``sanitize`` which defaults to ``True``. If it is true, each
	   tokenized sentence is sanitized (with your ``sanitize``-function) before
	   the state transition probabilities are computed.

	#. Create a function ``generate(state_transition_probabilities, length=10, start=None)``,
	   which returns a piece of text generated from given state transition
	   probabilities. The piece of text should be at most ``length`` tokens long
	   and concatenated into a single string. The
	   generation should end without an exception if a state that has no successors
	   is generated. If ``start`` is other than ``None``, the generation
	   should be started from that state. Handle the case where the state given
	   by ``start`` is not in the transition probabilities.

	#. Create a function ``likelihood(text, state_transitions_probabilities)`` 
	   that computes the likelihood of the text using the state transition
	   probabilities.


Week 2 - Markov Chains
----------------------

	#. Alter your function ``markov_chain`` from the first week to accept an optional
	   parameter ``order`` which specifies the order of the Markov chain to be
	   created. That is, with ``order=2`` a state contains two successive tokens
	   from the same sentence.
	
	#. Alter your function ``generate`` from the first week to be compatible with your
	   new ``markov_chain`` implementation. The returned piece of text should be
	   a single string with no repeating words, or nested arrays, etc.

	#. Experiment by generating text with different order Markov chains. What
	   observations do you make?