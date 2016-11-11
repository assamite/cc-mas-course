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

	#. `Geraint Wiggins - A preliminary framework for description, analysis and comparison of creative systems
	   <http://www.sciencedirect.com/science/article/pii/S0950705106000645>`_
	   (due Tue 15.11. 23.55)

	#. To be announced (due Tue 22.11. 23.55)
	#. To be announced (due Tue 29.11. 23.55)

Exercises
---------

.. centered::
	(Thu 10.11. 11.57) The weekly exercises were changed to be on their own
	pages. See below.

Weekly programming and theoretical exercise deadlines are on Sundays at 23.55
every week. The exercises marked with **RETURN** at the start,
will be the ones that accumulate your course points in Part 1 (and therefore
should be included in the compressed file).

**Weekly Exercises:**

	#. :doc:`ex_mc_parsing`
	#. :doc:`ex_mc_mas`
	#. Week 3 to be announced
	#. Week 4 to be announced

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
