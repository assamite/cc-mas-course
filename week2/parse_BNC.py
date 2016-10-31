'''
.. py:module:: 
    :platform: Unix

Parse `British National Corpus <http://www.natcorp.ox.ac.uk/>`_ for text and
POS-tags.

`Download it <http://ota.ox.ac.uk/desc/2554>`_

The code is not optimized in anyway, when using the whole corpus, the Python
program ends up using ~3.5GB of memory in the end! For example, it could be
profitable to train your model (Markov chain, etc.) straight when parsing each
document.
'''
from xml.etree import ElementTree as ET
import logging
import os
import pickle

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

TEXT_TYPE = 'FICTION' # Other text types include e.g. NEWS

# Root folder for Texts in the BNC. When testing, it is advised to you one of
# the sub-folders in Texts instead.
ROOT_FOLDER = "/Users/pihatonttu/corpora/2554/2554/download/Texts"


def parse_etree(etree):
    '''Parse element tree for tags 'w' and 'c' in their appearance order.

    See `basic structure <http://www.natcorp.ox.ac.uk/docs/URG/cdifbase.html>`_.

    :param etree: :py:class:`xml.etree.ElementTree`
    :returns list of (text, c5)-tuples, where c5 is the CLAWS C5 POS-tag.
    '''
    parsed = []
    for e in etree.iter():
        if e.tag == 'w' or e.tag == 'c':
            parsed.append((e.text, e.attrib['c5']))
    return parsed


def gather_xmls(root_folder):
    '''Get a list of .xml files in the root's subfolders.
    '''
    ret = os.walk(root_folder)
    filepaths = []
    for r in ret:
        fps = [os.path.join(r[0], e) for e in r[2] if e.endswith('.xml')]
        filepaths = filepaths + fps
    logger.info("Gathered {} files".format(len(filepaths)))
    return filepaths


if __name__ == '__main__':
    filepaths = gather_xmls(ROOT_FOLDER)
    texts = []

    for f in filepaths:
        logger.info("Reading: {}".format(f))
        etree = ET.parse(f)
        root = etree.getroot()
        text_type = root[1].attrib['type']
        if root[1].attrib['type'] != TEXT_TYPE:
            logger.info("Skipping {} (type={})".format(f, text_type))
        else:
            parsed = parse_etree(etree)
            texts = texts + parsed
            logger.info("Parsed {} tokens from {}. (Total {})"
                        .format(len(parsed), f, len(texts)))

    # Save the list as a pickle. Load it using pickle.load.
    with open('parsed_BNC.pkl', 'ab') as f:
        pickle.dump(texts, f)


