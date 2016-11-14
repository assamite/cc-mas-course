Week 3 - Multi-Agent Systems, Memory, Learning
=============================================================

	#. Familiarize yourself with the example of an agent with a limited memory
	   of lastly seen the artifacts  (see :doc:`mas_memory`). The next exercises
	   are heavily based on it.

	#. **RETURN** In the example (see previous exercise), the memory model is a very
	   concrete one, holding the lastly seen artifact instances as is. However,
	   as you might remember from the Ventura's paper from the first week, it
	   does not necessarily have to be. Instead, it could change the representation
	   of the artifacts to e.g. compress information to a more compact form.

	   Give some examples of concrete models that could be used as the memory
	   of an agent (you can think of any models you have previously encountered,
	   e.g. from machine learning or data mining). You can choose the domain of
	   the artifacts and its restrictions as you see fit as long as you state
	   them clearly in your answer. What pros and cons does your memory model have?
	   Write your answer shortly (10-15 sentences).

	   Additional notes:

		* The memory model does not have to strictly fit into the **memorize**
		  category in the Ventura's paper. Instead, it can have a flavor of
		  **generalize** category. The important part is that it should be able
		  to help in assessing the new artifact's novelty based on the previously
		  seen artifacts.

	#. **RETURN** Use memory model in your own code:

		* Adjust your agent class with the MC implementation to use the 
		  :class:`ListMemory` in the same way as in the example i.e. use it to
		  compute the novelty of an artifact and refactor :func:`evaluate` to
		  take into account both the novelty and the value. Value function can
		  be the same function you implemented the last week, or the
		  (pseudo)likelihood.

		* Adjust your :meth:`ToyEnvironment.vote` to add the winner's of the vote
		  to the domain as described in the example.
		
		* Add the memorization of both the agent's own artifacts and random
		  domain artifacts to :func:`act`.

	#. **RETURN** Towards transformational creativity
	
	   Background:
	
	   In this exercise, we will implement a simple functionality
	   which makes the agents adjust their generative model during their lifespan.
	   This functionality could be stated to be the first step towards the
	   transformational creativity (if we are pompous). The functionality is
	   implemented by changing (or adding to) the inner Markov chain representation
	   of the agent.

	   Until now, the agents have only needed their current state transition
	   probability data structures, which have been given or learned at the
	   initialization time, to generate new pieces of text. Now, we will go a step
	   backwards, and keep count of the actual number of each
	   state transition (i.e. ``state_transitions`` in the first week's example)
	   in each agent. That is, each agent should either learn the state transition
	   counts (**not** probabilities) from the given file at initialization time,
	   or they are given this data structure. 

	   Furthermore, each agent should have an access to
	   simple function which then transforms these state transitions counts into
	   probabilities. However, the state transition counts should be modifiable
	   at all times (and new transition probabilities computable).

	   We will update the state transition counts when the agent observes the
	   domain artifacts in :func:`act`. In the example, agent has a random access
	   to the previous vote winning artifacts (domain) which their currently
	   only memorize into their model. To modify our generative model, we add to the
	   agent's state transitions counts each state transition that is observed
	   from the domain artifact. Then, we update the state transition probabilities
	   based on the current state transition counts.

	   Specification:

	   Implement a method :meth:`learn(self, artifact)` in your agent
	   class. The method takes as input :class:`Artifact` object, and updates the
	   state transition counts with each state transition that is observed from
	   the artifact (remember that the actual string was in ``obj`` attribute
	   of the artifact object). Use appropriate tokenization method (depending
	   on your MC implementation) to split the string first and then observe the
	   state transitions from the tokenized string. The function (or some helper
	   function) then adds these state transitions to your state transition counts.
	   If new states and state transitions are observed, add them to the data
	   structure as well. Then, compute the new state transition probabilities
	   for the agent. Call this in :func:`act` for the domain artifact that was
	   memorized (if there was any domain artifacts).

	#. **RETURN** After you have built the functionality from the previous exercise,
	   run the simulation for an agent population with at least two different
	   sources of MC models. Observe if the transformational properties of the
	   agents affect the agents liking of the inner (agents with the same starting
	   MC model) or outer (agents with the different starting MC model) groups in the
	   long run. You may have to run the simulation quite a long time (some thousands of
	   iterations). What do you observe? State your findings shortly. You may
	   use plots, images or other visualization methods (in fact you are encouraged
	   to).

	   Additional notes:

		* Splitting the long run into even length intervals and computing some
		  aggregate measures from the voting behavior during each interval can
		  be a good starting point. However, you may do the observations any way
		  you like as long as you are able to extract some interesting bits of
		  information of what happens in the society during the system run (if
		  anything happens at all).
	
		* Try to be as elaborate as you can get in your observations. Why things
		  happen or do not happen?

	#. **RETURN** Design and implement an agent interaction model, where agents ask directly
	   others opinions about their artifacts and may take the information they
	   see viable into account by modifying their generative model or
	   evaluation function (or both). The interaction model does not have to be complex,
	   and the rules when the agents learn something from the feedback can be
	   simple. We have free rein of your own design! Write a short description of your model.
	   Return both the description and the code.