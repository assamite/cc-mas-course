'''
.. py:module:: markov_agent
    :platform: Unix

An example implementation of a creative agent which generates text with Nth
order Markov chains.
'''
import random

from creamas import CreativeAgent, Environment, Simulation, Artifact

import os
import operator
import re
import nltk

ORDER = 2

# Download Alice's Adventures in Wonderland if it is not yet present
alice_file = 'alice.txt'
alice_raw = None

if not os.path.isfile(alice_file):
    from urllib import request
    url = 'http://www.gutenberg.org/cache/epub/19033/pg19033.txt'
    response = request.urlopen(url)
    alice_raw = response.read().decode('utf8')
    with open(alice_file, 'w', encoding='utf8') as f:
        f.write(alice_raw)
else:
    with open(alice_file, 'r', encoding='utf8') as f:
        alice_raw = f.read()

# Remove the start and end bloat from Project Gutenberg (this is not exact, but
# easy).
pattern = r'\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .+ \*\*\*'
end = "End of the Project Gutenberg"
start_match = re.search(pattern, alice_raw)
if start_match:
    start_index = start_match.span()[1] + 1
else:
    start_index = 0
end_index = alice_raw.rfind(end)
alice = alice_raw[start_index:end_index]

# And replace more than one subsequent whitespace chars with one space
alice = re.sub(r'\s+', ' ', alice)

def _sanitize(tokenized_sentences):
    is_word = re.compile('\w')
    sanitized_sentences = []
    for sent in tokenized_sentences:
        sanitized = [token for token in sent if is_word.search(token)] + ['.']
        sanitized_sentences.append(sanitized)
    return sanitized_sentences


def tokenize(raw_text, sanitize=True):
    '''Tokenize raw text to sentences and then each sentences to individual
    tokens (words).
    '''
    # Tokenize the text into sentences.
    sentences = nltk.sent_tokenize(raw_text)

    # Tokenize each sentence to words. Each item in 'words' is a list with
    # tokenized words from that list.
    tokenized_sentences = []
    for s in sentences:
        w = nltk.word_tokenize(s)
        tokenized_sentences.append(w)

    if sanitize is True:
        tokenized_sentences = _sanitize(tokenized_sentences)
    return tokenized_sentences

def get_transitions(tokenized_sentences):
    '''Compute the state transition counts from the tokenized sentences.
    '''
    transitions = {}
    # TODO: make this work!
    for sentence in tokenized_sentences:
        for i in range(len(sentence)-ORDER):
            pred = tuple(sentence[i:i+ORDER])
            succ = tuple(sentence[i+1:i+1+ORDER])
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
    return transitions

def get_probabilities(transitions):
    '''Compute state transition probabilities from the state transition counts.
    '''

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
    return probs

def markov_chain(raw_text):
    tokenized_sentences = tokenize(raw_text)
    transitions = get_transitions(tokenized_sentences)
    probs = get_probabilities(transitions)
    return probs

class MarkovAgent(CreativeAgent):
    '''An agent that generates text with a Markov chain.
    '''
    def __init__(self, env, stp, n=20):
        '''
        :param env: class:`~creamas.core.environment.Environment`
        :param stp:
            MC state transition probabilities. Data structure should contain
            two nested dictionaries. Outer dictionary is a mapping from
            preceding states to dictionaries and each preceding state's
            dictionary is a mapping from successive states to their
            probabilities, i.e ``stp[prec][succ]`` will give you probability
            for the state transition from state ``prec`` to state ``succ``.

            The states should be tuples of strings and all tuples should have
            the same length (all states are of same order).
        :param int n:
            Search width, i.e. how many alternatives are considered per call to
            :meth:`invent`.
        '''
        super().__init__(env)
        self._stp = stp
        # This is the order of the Markov chain in _stp
        self._order = len(list(self._stp.keys())[0])
        self._n = n
        name = self.name
        self.name = "{}({})".format(self.__class__.__name__, name)

    def generate(self, length=10, start=None):
        '''Generate new piece of text.

        Generated text is at most **length** tokens long. Generation stops if
        a state with no successors is generated.

        :param int length: Length of the text in tokens.
        :param start:
            Starting state for the generation. **None** if starting state
            should be random.
        :type start: A valid state for the MC (tuple of strings)
        :returns: Generated text.
        '''
        if start is not None and start not in self._stp:
            raise LookupError("Given starting state '{}' not in transition "
                             "probabilities (_stp).".format(start))
        if start is None:
            start = random.choice(list(self._stp.keys()))

        gen = ' '.join(start)
        k = len(start)
        prec = start
        for _ in range(length-k):
            if prec not in self._stp:
                return gen
            probs = self._stp[prec]
            base = 0.0
            rng = random.random()
            for succ, value in probs.items():
                base += value
                if rng < base:
                    gen += " {}".format(succ[-1])
                    prec = succ
                    break
        return gen

    def evaluate(self, artifact):
        '''Evaluate the artifact (piece of text) by computing the likelihood 
        it was generated from the agent's state transition probabilities.

        The first state is assumed to be given. If the artifact contains states
        (or state transitions) not in the state transition probabilities, we
        will give them a small random value (in [0, 0.001]).

        :param artifact:
            `~creamas.core.artifact.Artifact`, for which holds
            ``type(artifact.obj)==str``.
        :returns:
            (likelihood, framing)-tuple, where the framing is ``None``.
        '''
        text = artifact.obj
        states = self._parse_states(text)
        lh = self._likelihood(states)
        return lh, None

    def _parse_states(self, text):
        '''Secret function the user should not have to care of.
        '''
        tokens = text.split()
        # Order of the MC is the length of its states
        o = self._order
        # Text does not contain viable states.
        if len(tokens) < o:
            return None
        # Gather a state list
        return list(map(lambda x: tuple(tokens[x:x+o]), range(len(tokens)-o+1)))

    def _likelihood(self, states):
        '''Secret likelihood evaluation. Assigns a small random value to the
        state transitions that are not in the current state transition
        probabilities.
        '''
        lh = 1.0
        for i in range(len(states[:-1])):
            prob = random.random() * 0.001
            prec = states[i]
            succ = states[i+1]
            if prec in self._stp and succ in self._stp[prec]:
                prob = self._stp[prec][succ]
            lh *= prob
        return lh

    def invent(self, n):
        '''Invent a new artifact by generating **n** artifacts and selecting
        the best one.

        Selection is done based on :meth:`evaluate`.

        :param int n: The number of alternative artifacts generated
        :returns:
            :class:`~creamas.core.artifact.Artifact`, the best artifact based
            on :meth:`evaluate`
        '''
        g = self.generate()
        best_artifact = Artifact(self, g)
        best_eval, _ = self.evaluate(best_artifact)
        for _ in range(n-1):
            g = self.generate()
            artifact = Artifact(self, g)
            evl, _ = self.evaluate(artifact)
            if evl > best_eval:
                best_artifact = artifact
                best_eval = evl
        best_artifact.add_eval(self, best_eval)
        return best_artifact, best_eval

    async def act(self):
        '''Invent new artifact and add it to the environment's candidate
        artifacts.
        '''
        artifact, e = self.invent(self._n)
        print("{}: Invented artifact '{}' (eval={})"
              .format(self.name, artifact.obj, e))
        self.env.add_candidate(artifact)


if __name__ == "__main__":
    probs = markov_chain(alice)
    env = Environment.create(('localhost', 5555))
    ma = MarkovAgent(env, probs, n=20)
    t = ma.generate(length=10)
    print("generated: {}".format(t))
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ma.act())