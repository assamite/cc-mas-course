'''
.. py:module:: parsing_nltk
    :platform: Unix

Sample code to parse written text to a more appropriate form. This code is
designed to be used to create state transitions for Markov chains.
'''
import os
import re
import nltk

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

# For reasons, lets remove the start and end bloat from the text
start = "I--DOWN THE RABBIT-HOLE"
end = "End of the Project Gutenberg"
start_index = alice_raw.find(start)
end_index = alice_raw.rfind(end)
alice = alice_raw[start_index:end_index]

# And replace more than one subsequent whitespace chars with one space
alice = re.sub(r'\s+', ' ', alice)

# Tokenize the text into sentences.
sentences = nltk.sent_tokenize(alice)

# Tokenize each sentence to words. Each item in 'words' is a list with
# tokenized words from that list.
tokenized_sentences = []
for s in sentences:
    w = nltk.word_tokenize(s)
    tokenized_sentences.append(w)

# Next, we sanitize the 'words' somewhat. We remove all tokens that do not have
# any Unicode word characters, and force each sentence's last token to '.'.
# You can try other sanitation methods (e.g. look at the last sentence).
is_word = re.compile('\w')
sanitized_sentences = []
for sent in tokenized_sentences:
    sanitized = [token for token in sent if is_word.search(token)] + ['.']
    sanitized_sentences.append(sanitized)

# Now we are ready to create the state transitions. However, this time we
# count the state transitions from each sentence at a time.
transitions = {}
# TODO: make this work!








