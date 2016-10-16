Parsing Text with NLTK
======================

`(full code) <https://github.com/assamite/cc-mas16/blob/master/week1/parsing_nltk.py>`_

In this section we will parse a long written text, everyone's favorite tale
*Alice's Adventures in  Wonderland* by Lewis Carroll, to be used to create the 
state transitions for Markov chains. In this example, we use
`NLTK <http://www.nltk.org/>`_ for natural language processing (refer to
`book <http://www.nltk.org/book/>`_ for clearer instructions on usage).
However, many of the parsing tasks using NLTK could be adequately achieved with
sufficiently simple regular expressions.

.. note:: 
	NLTK should be installed in your environment. It is contained in the
	``requirements.txt``. To install it separately use ``pip install nltk``
	while your virtual environment is activated.

Downloading the Data
--------------------

First, we need to get the data. Fortunately, our book of choice is served on
`Project Gutenberg <https://www.gutenberg.org/>`_, which offers thousands
of free books. Natural choice is to download the book inside our script.
However, to make the part little bit more interesting, we are going to download
it only once, and then, if the file is already present, we read it from the
file. ::

	import os
	import re

	import nltk

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

Remove the Excessive Parts
--------------------------

Now, we have the raw version of the book. Next, we are going to remove the
"bloat" that Project Gutenberg adds to the beginning and the end of the book. ::

	# For reasons, lets remove the start and end bloat from the text
	start = "I--DOWN THE RABBIT-HOLE"
	end = "End of the Project Gutenberg"
	start_index = alice_raw.find(start)
	end_index = alice_raw.rfind(end)
	alice = alice_raw[start_index:end_index]
	
	# And replace more than one subsequent whitespace chars with one space
	alice = re.sub(r'\s+', ' ', alice)

Tokenize the text
-----------------

Our text is now ready to be tokenized with NLTK. First, we are going to split it
into sentences, which is easy with the tools NLTK offers::

	sentences = nltk.sent_tokenize(alice)

Next, we are going to tokenize each sentence using ``nltk.word_tokenize``, which
splits the text into 'words' (it also splits punctuation into separate tokens).
Here is an example of its output::

	>>> nltk.word_tokenize('Follow the "White Rabbit".')
	['Follow', 'the', '``', 'White', 'Rabbit', "''", '.']

Here is the actual tokenization code::

	tokenized_sentences = []
	for s in sentences:
	    w = nltk.word_tokenize(s)
	    tokenized_sentences.append(w)

Another often used NLP task is part-of-speech (POS) tagging. We are not going
to use it for now, but it is as simple as tokenization::

	>>> tokens = nltk.word_tokenize('Follow the "White Rabbit".')
	>>> nltk.pos_tag(tokens)
	[('Follow', 'VB'),
	 ('the', 'DT'),
	 ('``', '``'),
	 ('White', 'NNP'),
	 ('Rabbit', 'NNP'),
	 ("''", "''"),
	 ('.', '.')]

.. note::
	``nltk.pos_tag`` needs a pos-tagger which does not come bundled with basic
	nltk-version. To download a pos-tagger, type ``nltk.download()`` in iPython
	and download the Averaged Perceptron Tagger from Models-section. Download
	tool offers many usable models and corporas.

Sanitation of the Tokenized Sentences
-------------------------------------

Lastly, we sanitize the tokenized sentences a bit so that the punctuation does
not clutter the Markov chains. For this purpose, we naively assume that any
token in the sentences is a proper word, if it contains any Unicode word
character. We also end all the sentences with a dot, to mark a natural pause
in the text (one could also add a special token to the beginning). ::

	is_word = re.compile('\w')
	sanitized_sentences = []
	for sent in tokenized_sentences:
	    sanitized = [token for token in sent if is_word.search(token)] + ['.']
	    sanitized_sentences.append(sanitized)

Now, the ``sanitized_sentences`` should be ready for the creation of state
transition probabilities. However, it is left as an exercise together with the
actual generation of texts.

