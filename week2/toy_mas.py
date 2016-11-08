'''
.. py:module:: toy_mas
    :platform: Unix

Toy example of using `creamas <https://github.com/assamite/creamas/>`_ to build
a multi-agent system.
'''
from collections import Counter
import logging
import random
import re

import aiomas

from creamas.core import CreativeAgent, Environment, Simulation, Artifact

# Logging setup. This is simplified setup as all agents use the same logger.
# It _will_ cause some problems in asynchronous settings, especially if you
# are logging to a file.
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def levenshtein(s, t):
        '''Compute the edit distance between two strings.

        From Wikipedia article; Iterative with two matrix rows.
        '''
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]

        return v1[len(t)]


def parse_words(filename, encoding, word_pattern, wlen_limits):
    '''Parse acceptable words from the file.

    :param str filename: Path to the file to parse
    :param str encoding: Encoding of the file (most probably 'utf8')
    :param word_pattern: Compiled regex for acceptable words
    :param tuple wlen_limits: Length limits for the acceptable words
    :returns:
        Acceptable words as a list (may contain multiple entries of the same
        word).
    '''
    # Filter function to define which words are accepted.
    def is_word(w):
        if not word_pattern.match(w.lower()):
            return False
        if not len(w) >= wlen_limits[0]:
            return False
        if not len(w) <= wlen_limits[1]:
            return False
        return True

    with open(filename, 'r', encoding=encoding) as f:
        content = f.read()
        words = content.split()
    ret = [w.lower() for w in words if is_word(w)]
    return ret


def frequent_words(filename, encoding, word_pattern, wlen_limits, n=20):
    '''Get the most frequent words from the given file.

    The 'word' is used loosely here as a word is anything the ``parse_words``
    function will recognize as a word.

    :param str filename: File to learn the words
    :param str encoding: Encoding of the file (most probably 'utf8')
    :param word_pattern: Compiled regex for acceptable words
    :param tuple wlen_limits: Length limits for the acceptable words
    :param int n: Number of words to return
    :returns: a list of the most common (n) words in the file
    '''
    words = parse_words(filename, encoding, word_pattern, wlen_limits)
    # Count the number of times each element appears in the list
    ctr = Counter(words)
    common = ctr.most_common(n)
    # return only the words, not their counts
    return [e[0] for e in common]


class ToyAgent(CreativeAgent):
    '''A sample agent implementation.

    Agent invents new words be generating them at random and evaluating them
    with respect to its own vocabulary. 

    Agent learns its vocabulary from the file given at initialization.
    '''

    def __init__(self, env, filename, encoding='utf8', n=20,
                 wlen_limits=(2,11), chars='abcdefghijklmnopqrstuvwxyz'):
        '''
        :param env:
            subclass of :py:class:`~creamas.core.environment.Environment`

        :param str filename: Filename from which the words should be parsed.
        :param str encoding: Encoding of the file

        :param int n:
            The number of words the agent considers per :func:`invent`

        :param tuple wlen_limits:
            (int, int)-tuple, acceptable word length limits

        :param str chars: acceptable characters in the words
        '''
        super().__init__(env)
        self.n = n
        self.chars = chars
        self.wlen_limits = wlen_limits
        self.word_pattern = re.compile(r'^\w+$')
        self.vocab = frequent_words(filename, encoding=encoding,
                                    word_pattern=self.word_pattern,
                                    wlen_limits=self.wlen_limits, n=20)

    def evaluate(self, artifact):
        '''Evaluate given artifact with respect to the words the agent knows.

        Actual evaluation formula for a string :math:`s` is:

        .. math::
            e(s) = \\max_{w \in \\texttt{vocab}}\\frac{1 - \\texttt{lev}(s, w)}
            {\\max(|s|, |w|)},

        where :math:`\\texttt{lev}(s, w)` is the Levenshtein
        distance between the two strings.

        :param artifact: :class:`~creamas.core.Artifact` to be evaluated
        :returns:
            (evaluation, word)-tuple, containing both the evaluation and the
            word giving the maximum evaluation
        '''
        evaluation = 0.0
        evaluation_word = artifact.obj
        matching_word = self.vocab[0]
        for word in self.vocab:
            lev = levenshtein(evaluation_word, word)
            mlen = max(len(evaluation_word), float(len(word)))
            current_evaluation = 1.0 - (float(lev) / mlen)
            if current_evaluation > evaluation:
                evaluation = current_evaluation
                matching_word = word
        return evaluation, matching_word

    def generate(self):
        '''Generate a new word.

        Word is generated by uniformly drawing from ``chars``. Word length is
        in ``wlen_limits``.

        :returns: a word wrapped as :class:`~creamas.core.artifact.Artifact`
        '''
        word_length = random.randint(*self.wlen_limits)
        word = [random.choice(self.chars) for _ in range(word_length)]
        word = ''.join(word)
        return Artifact(self, word, domain=str)

    def invent(self, n=20):
        '''Invent a new word.

        Generates multiple (n) words and selects the one with the highest
        evaluation.

        :param int n: Number of words to consider
        :returns:
            a word wrapped as :class:`~creamas.core.artifact.Artifact` and its
            evaluation.
        '''
        best_artifact = self.generate()
        max_evaluation, match_word = self.evaluate(best_artifact)
        for _ in range(n-1):
            artifact = self.generate()
            evaluation, m_word = self.evaluate(artifact)
            if evaluation > max_evaluation:
                best_artifact = artifact
                max_evaluation = evaluation
                match_word = m_word
        logger.debug("{} invented word: {} (eval={}, match={})"
                     .format(self.name, best_artifact.obj, max_evaluation,
                             match_word))
        # Add evaluation and framing to the artifact
        best_artifact.add_eval(self, max_evaluation, fr={'match' : match_word})
        return best_artifact


    async def act(self):
        '''Agent acts by inventing new words.
        '''
        artifact = self.invent(self.n)
        self.env.add_candidate(artifact)



class ToyEnvironment(Environment):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def vote(self, age):
        artifacts = self.perform_voting(method='mean')
        if len(artifacts) > 0:
            accepted = artifacts[0][0]
            value = artifacts[0][1]
            logger.info("Vote winner by {}: {} (val={})"
                        .format(accepted.creator, accepted.obj, value))
        else:
            logger.info("No vote winner!")

        self.clear_candidates()


if __name__ == "__main__":
    filename = '../week1/alice.txt'
    env = ToyEnvironment.create(('localhost', 5555))
    for i in range(10):
        agent = ToyAgent(env, filename=filename)

    sim = Simulation(env, log_folder='logs', callback=env.vote)
    sim.async_steps(10)
    sim.end()