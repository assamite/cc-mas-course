Agents With Memory and Learning From Domain
============================================

`(full code) <https://github.com/assamite/cc-mas-course/blob/master/week3/mas_memory.py>`_

.. warning::
	This example is written for Creamas version 0.1.1. If you want to be sure
	you have the right version, type in terminal (when you have virtual environment
	activated): ``pip install --upgrade creamas==0.1.1``

This week we will build a simple memory for our agents and use it to memorize
agent's own artifacts and artifacts from the domain. However, we will strictly
restrict the memory size in order to effectively model the resource restrictions
of each individual agent (with unlimited memory, and certain communication
structures the agents would not have local views any more as they more or less
would have the full knowledge of what the whole society has created before).

In this example, we will use the memory model to directly assess the novelty of
artifacts. However, it could also be used in other ways.

Memory Model
------------

Our memory model will be a simple list which we will wrap as a class to get
a clean API for it (and which would allow us to switch memory models
easily if other models would use the same API). For our memory model, we
actually only define one method: :meth:`memorize` which will memorize a new artifact
into a memory and possibly forget some other (i.e. the oldest) artifact from
the memory if it is full. The initialization method will have one parameter, ``capacity``,
which will be the maximum number of artifacts in the memory at any single time. 
::

	class ListMemory():
	    '''Simple list memory which stores all seen artifacts as is into a list.
	    '''
	    def __init__(self, capacity):
	        '''
	        :param int capacity: The maximum number of artifacts in the memory.
	        '''
	        self._capacity = capacity
	        self._artifacts = []
	
	    @property
	    def capacity(self):
	        '''The maximum number of artifacts in the memory.
	        '''
	        return self._capacity
	
	    @property
	    def artifacts(self):
	        '''The artifacts currently in the memory.
	        '''
	        return self._artifacts
	
	    def memorize(self, artifact):
	        '''Memorize an artifact into the memory.
	
	        If the artifact is already in the memory, does nothing. If memory
	        is full and a new artifact is memorized, forgets the oldest artifact.
	
	        :param artifact: Artifact to be learned.
	        :type artifact: :class:`~creamas.core.artifact.Artifact`
	        '''
	        if artifact in self._artifacts:
	            return
	
	        self._artifacts.insert(0, artifact)
	        if len(self._artifacts) > self.capacity:
	            self._artifacts = self._artifacts[:self.capacity]

.. note::
	Some Python details. Skip if you are not interested.

	We have defined ``capacity`` and ``artifacts`` as properties (``@property``
	function decorator) without setters.
	This encourages the user of the class to not change them during
	:class:`ListMemory` object's life time. However, one could still access the
	``_capacity`` and ``_artifacts`` attributes, or even insert new artifacts
	into ``artifacts`` as it is not directly setting a new object as the property::

		>>> lm = ListMemory(10)
		>>> lm.capacity
		10
		>>> lm._capacity = 15
		>>> lm.capacity
		15
		>>> lm.capacity = 14
		Traceback (most recent call last):
  		  File "<stdin>", line 1, in <module>
		AttributeError: can't set attribute
		>>> lm.artifacts.insert(0, 'foo')
		>>> lm.artifacts
		['foo']

	To add a setter into a property we could define it for ``capacity`` as follows::

	    @capacity.setter
	    def capacity(self, cap):
	        assert type(cap) == int
	        assert cap > 0
	        self._capacity = cap

	The assertions would then cause an error if a user would try to set
	``capacity`` to something else than integer that is strictly positive.
	(Typically you would like to have more informative errors than :exc:`AssertionError`,
	but this will do for the sake of the example.)

Add :class:`ListMemory` to :class:`ToyAgent`
-------------------------------------------------

Next, we will fit the memory model into our :class:`ToyAgent` class from last
week and use it to assess the novelty of a new artifact. To this end we will:

	#. Change :func:`__init__`;
	#. Rename :func:`evaluate` to :func:`value` (and change its docstring a bit);
	#. Implement a new function :func:`novelty`;
	#. Re-implement :func:`evaluate`; 
	#. Modify :func:`invent` a bit to reflect the changes above; and
	#. Memorize every artifact the agent invents (i.e. one artifact per :func:`act`).

.. note::
	One could also acquire these changes by inheriting :class:`ToyAgent` from
	the last week and changing the appropriate parts, but we will not do
	it in this example for the sake of modularity.

Change :func:`__init__`
.......................

We change :func:`__init__` to also create the memory for the agent. This is done
simply by adding the following line in it::

	self.mem = ListMemory(20)

Rename :func:`evaluate` to :func:`value`
........................................

As :func:`evaluate` is a reserved function in Creamas which some of the other
library functionality calls inherently (e.g. :func:`CreativeAgent.vote`), we need to keep it as the highest level
evaluation function. As we will introduce a new evaluation function :func:`novelty`,
we need to use :func:`evaluate` to combine the two different evaluations. To this
end we simply rename our old :func:`evaluate` to :func:`value` to remind us that
it is the function that evaluates how valuable each artifact is.

Implement a New Function :func:`novelty`
........................................

Next, we will implement a new function :func:`novelty`. It is very similar to :func:`value`
function, but it compares the new artifact to the artifacts in the memory, not
in the vocabulary, and it computes the novelty of an artifact to be the **minimum**
distance between the artifact and any artifact in the memory. Here is its
documentation:

.. automethod:: mas_memory.ToyAgent.novelty

And here is its code (docstring omitted)::

    def novelty(self, artifact):
        # We will choose that the novelty is maximal if agent's memory is empty.
        if len(self.mem.artifacts) == 0:
            return 1.0, None

        novelty = 1.0
        evaluation_word = artifact.obj
        matching_word = self.mem.artifacts[0].obj
        for memart in self.mem.artifacts:
            word = memart.obj
            lev = levenshtein(evaluation_word, word)
            mlen = max(len(evaluation_word), float(len(word)))
            current_novelty = float(lev) / mlen
            if current_novelty < novelty:
                novelty = current_novelty
                matching_word = word
        return novelty, matching_word


Re-Implement :func:`evaluate`
.............................

Our new :func:`evaluate` will take both :func:`value` (the renamed
:func:`evaluate` from the last week) and :func:`novelty` into consideration:

.. automethod:: mas_memory.ToyAgent.evaluate


Here is its code (docstring omitted)::

    def evaluate(self, artifact):
        value, value_framing = self.value(artifact)
        novelty, novelty_framing = self.novelty(artifact)
        framing = {'value': value_framing, 'novelty':novelty_framing}
        evaluation = (value + novelty) / 2
        return evaluation, framing

Modify :meth:`invent`
.....................

We modify :func:`invent` by explicitly renaming the framing returned by
:meth:`evaluate` (the second element in the returned tuple) as ``framing``.

Here is the new code::

    def invent(self, n=20):
        best_artifact = self.generate()
        max_evaluation, framing = self.evaluate(best_artifact)
        for _ in range(n-1):
            artifact = self.generate()
            evaluation, fr = self.evaluate(artifact)
            if evaluation > max_evaluation:
                best_artifact = artifact
                max_evaluation = evaluation
                framing = fr
        logger.debug("{} invented word: {} (eval={}, framing={})"
                     .format(self.name, best_artifact.obj, max_evaluation,
                             framing))
        # Add evaluation and framing to the artifact
        best_artifact.add_eval(self, max_evaluation, fr=framing)
        return best_artifact

Memorize Artifacts
..................

Now, we have our memory model fitted into our agent, but we do not yet memorize
any artifacts. To this end, we will first memorize all the artifacts the agent
itself invents by modifying :meth:`act`::

    async def act(self):
        '''Agent acts by inventing new words.
        '''
        artifact = self.invent(self.n)
        self.mem.memorize(artifact)
        self.env.add_candidate(artifact)

Memorization from Domain
------------------------

Until now, the agents have only memorized their own artifacts. To make our agent
society really intertwined, we want the agents to memorize (part of the) artifacts generated
by other agents. To this end we will gather a domain of former vote winners in the
environment, and let the agents memorize a random artifact from the domain on
each :meth:`act`. This is again very simple method, but will do for the sake of
the example

Populating the Domain
.....................

Populating the domain is easy in Creamas as the environment already has some
suitable methods for it. We will just add the votes winner(s) after each vote
to the domain. As we already call :func:`ToyEnvironment.vote` after every iteration,
we will modify it. ::

    def vote(self, age):
        artifacts = self.perform_voting(method='mean')
        if len(artifacts) > 0:
            accepted = artifacts[0][0]
            value = artifacts[0][1]
            self.add_artifact(accepted) # Add vote winner to domain
            logger.info("Vote winner by {}: {} (val={})"
                        .format(accepted.creator, accepted.obj, value))
        else:
            logger.info("No vote winner!")
        self.clear_candidates()

Memorizing the Domain Artifacts
...............................

Each agent will memorize one random domain artifact on during each :func:`act`.
For this, we will add two lines at the start of the :func:`act`::

	if len(self.env.artifacts) > 0:
		self.mem.memorize(random.choice(self.env.artifacts))

Making the whole function look like this::

    async def act(self):
        if len(self.env.artifacts) > 0:
            self.mem.memorize(random.choice(self.env.artifacts))
        artifact = self.invent(self.n)
        self.mem.memorize(artifact)
        self.env.add_candidate(artifact)

First we memorize a new domain artifact, then, we invent a new artifact
and memorize it, and lastly, we add our invented artifact to the voting candidates
for this iteration.

Running the Simulation
----------------------

Running the simulation happens exactly like in the last week's example.
In short::

	if __name__ == "__main__":
	    filename = '../week1/alice.txt'
	    env = ToyEnvironment.create(('localhost', 5555))
	    for i in range(10):
	        agent = ToyAgent(env, filename=filename)
	
	    sim = Simulation(env, log_folder='logs', callback=env.vote)
	    sim.async_steps(10)
	    sim.end()