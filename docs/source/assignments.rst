Assignments
===========

Assignments for the first part of the course. The group project instructions
to be added elsewhere.

.. warning:: 
	All assignments are returned through
	`Moodle <https://moodle.helsinki.fi/course/view.php?id=22439>`_
	(course key: ccmas2016). Do **not** send them by email!

**Preliminaries:**

	#. Set the development environment (see :doc:`setup`)

		- Install Python 3.5
		- Create a virtual environment
		- Install ``requirements.txt``

	#. Get used to Python (see :doc:`learn_python`). Things to consider
	   include:

		- Basic syntax: loops, lists, dictionaries, ``def``, ``class``,
		  ``import``, etc.
		- What does ``__init__``-function do for the classes? (see, e.g.
		  `Data Model <https://docs.python.org/3.5/reference/datamodel.html#special-method-names>`_)
		- How to run Python programs from the command line?

Essays
------

Each week there is an article to be read, and the students write a short essay
(**max** 250 words) summarizing its main points. The deadlines to the essays
are on Tuesdays at 23.55. Include your UH user name and student number to the
pdf!

.. note::
	Exception: First week's essay deadline is on Thursday 3.11. at 23.55!

**Essay articles:**

	#. `Dan Ventura - Mere generation: Essential barometer or dated concept?
	   <http://www.computationalcreativity.net/iccc2016/wp-content/uploads/2016/01/Mere-Generation.pdf>`_
	   (due Thu 3.11. 23.55)

	#. `Rob Saunders and Oliver Bown - Computational Social Creativity
	   <https://www.researchgate.net/publication/281143442_Computational_Social_Creativity>`_
	   (due Tue 8.11. 23.55)

	#. To be announced (due Tue 15.11. 23.55)
	#. To be announced (due Tue 22.11. 23.55)
	#. To be announced (due Tue 29.11. 23.55)

Exercises
---------

Weekly programming and theoretical exercise deadlines are on Sundays at 23.55
every week. The exercises marked with **RETURN** at the start,
will be the ones that accumulate your course points in Part 1 (and therefore
should be included in the compressed file).

Remember to return the exercises through Moodle. The exercises should be in
one compressed file which extracts to a folder with your UH user name. That is,
if your user name in UH is ``cthulhu`` and you return a file ``cthulhu_w1.tar.gz``, then
it should extract to, for example, the following structure::

	cthulhu/
		ex1.py
		ex2.py
		README # General info if needed
		some_file.txt


.. note::
	Document your code! `Sphinx <http://www.sphinx-doc.org>`_ is a good option
	for documentation in Python projects. `A short introduction to Sphinx
	<https://pythonhosted.org/an_example_pypi_project/sphinx.html>`_.

	This documentation has been created using Sphinx, so you may look at the
	repository's ``docs/source``-folder for some tips also. However, you do not
	have to build the documentation when returning the exercises. Making a
	short docstring for main functions and classes (and modules) is enough.


Week 1 - Markov Chains, Parsing
...............................

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


Week 2 - Markov Chains
......................

	.. note:: 
		These are currently pending and subject to change.

	#. **RETURN** Alter your function ``markov_chain`` from the first week to
	   accept an optional parameter ``order`` which specifies the order of the
	   Markov chain to be created. That is, with ``order=2`` a state contains
	   two successive tokens from the same sentence.
	
	#. **RETURN** Alter your function ``generate`` from the first week to be compatible with your
	   new ``markov_chain`` implementation (from the exercise 1. in this week).
	   The returned piece of text should be a single string with no repeating
	   words, or nested arrays, etc.

	#. Experiment by generating text with different order Markov chains. What
	   observations do you make?
