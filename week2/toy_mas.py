'''
.. py:module:: toy_mas
    :platform: Unix

Toy example of using `creamas <https://github.com/assamite/creamas/>`_ to build
a multi-agent system.
'''
from collections import Counter
import random
import re

import aiomas

from creamas.core import CreativeAgent, Environment, Simulation, Artifact


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


class ToyAgent(CreativeAgent):

    def __init__(self, env, filename, encoding='utf8', n=20):
        super().__init__(env)
        self.word_pattern = re.compile(r'^\w+$')
        self.words = self.frequent_words(filename, enconding=encoding, n=n)
        c = 'abcdefghijklmnopqrstuvwxyz'
        self.chars = c
        self.wlen_limits = [2, 11]:

    def __parse_words(self, filename, encoding):
        # Filter function to define which words are accepted.
        def is_word(w):
            if not self.word_pattern.match(w.lower()):
                return False
            if not len(w) >= self.wlen_limits[0]:
                return False
            if not len(w) <= self.wlen_limits[1]:
                return False
            return True

        with open(filename, 'r') as f:
            content = f.read()
            words = content.split()
        ret = [w.lower() for w in words if is_word(w)]
        return ret

    def frequent_words(self, filename, encoding, n=20):
        '''Get the most frequent words from the given file.

        The 'word' is used loosely here as a word is anything the inner parsing
        function will recognize as a word.

        :param str filename: File to learn the words
        :param int n: Number of words to return
        :returns: a list of most common words in the file
        '''
        words = self.__parse_words(filename, encoding)
        # Count the number of times each element appears in the list
        ctr = Counter(words)
        common = ctr.most_common(n)
        # return only the words, not their counts
        return [e[0] for e in common]

    def evaluate(self, artifact):
        '''Evaluate given artifact with respect to the words the agent knows.

        Actual evaluation formula for artifact :math:`a` is:
        :math:`e(a) = \max_{w \in \textt{words}}{1 - \textt{lev}(a, w) /
        \max{|s|, |w|}}`, where :math:`\textt{lev}(a, w)` is the Levenshtein
        distance between the two string.

        :param artifact: `~creamas.core.Artifact` to be evaluated
        :returns:
            (evaluation, word)-tuple, containing both the evaluation and the
            word giving the maximum evaluation
        '''
        evaluation = 0.0
        evaluation_word = artifact.obj
        matching_word = self.words[0]
        for word in self.words:
            lev = levenshtein(evaluation_word, word)
            mlen = max(len(evaluation_word), float(len(word)))
            current_evaluation = 1.0 - (float(lev) / mlen)
            if current_evaluation > evaluation:
                evaluation = current_evaluation
                matching_word = word
        return evaluation, matching_word

    def create(self):
        word_length = random.randint(*self.wlen_limits)
        word = [random.choice(self.chars) for _ in range(word_length)]
        return Artifact(word)


    def invent(self, n=20):
        for i in range(n):
            pass

    async def act(self):
        artifact = self.invent_word()
        self.


class ToyEnvironment(Environment):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    filename = '../week1/alice.txt'
    env = ToyEnvironment()
    for i in range(10):
        agent = ToyAgent(env, filename=filename)

    sim = Simulation(env)
    sim.async_steps(10)
    sim.end()